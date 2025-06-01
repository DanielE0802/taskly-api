from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from auth.utils import BearerJWT, get_current_user_id
from database import execute_query, execute_update
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from projects.models import ProyectoOut, ProyectoCreate, ProyectoUpdate, UsuarioProyectoCreate
from typing import List, Optional

router = APIRouter()

def _get_project_with_users(id_proyecto: int):
    """
    Retorna un proyecto con su lista de usuarios asociados.
    """
    query_project = """
    SELECT id_proyecto, nombre_proyecto, descripcion_proyecto, id_usuario
    FROM Proyecto WHERE id_proyecto = %s
    """
    proyecto = execute_query(query_project, (id_proyecto,), fetchone=True)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    query_users = """
    SELECT
        up.id_usuario,
        u.nombre_usuario,
        up.rol_usuario_proyecto
    FROM Usuario_Proyecto up
    JOIN Usuario u ON up.id_usuario = u.id_usuario
    WHERE up.id_proyecto = %s;
    """
    usuarios = execute_query(query_users, (id_proyecto,), fetchall=True)
    proyecto["usuarios"] = usuarios
    return proyecto

def _get_user_projects_ids(user_id: int) -> List[int]:
    """
    Recupera la lista de project IDs a los que pertenece un usuario.
    """
    query = "SELECT id_proyecto FROM Usuario_Proyecto WHERE id_usuario = %s;"
    rows = execute_query(query, (user_id,), fetchall=True)
    return [r["id_proyecto"] for r in rows] if rows else []

def _fetch_project_by_id(id_proyecto: int) -> dict:
    """
    Obtiene un proyecto por su ID sin verificar permisos.
    """
    query = """
        SELECT
            id_proyecto,
            nombre_proyecto,
            descripcion_proyecto,
            id_usuario
        FROM Proyecto
        WHERE id_proyecto = %s;
    """
    result = execute_query(query, (id_proyecto,), fetchone=True)
    if result is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return result

def _assert_owner(id_proyecto: int, user_id: int) -> None:
    """
    Verifica que el usuario sea owner del proyecto.
    """
    proyecto = _fetch_project_by_id(id_proyecto)

    if proyecto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")

    # TODO: validar por tener varios administradores
    if proyecto["id_usuario"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar este proyecto"
        )

@router.post(
    "/",
    response_model=ProyectoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo proyecto"
)
def create_project(
    proyecto_in: ProyectoCreate,
    credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())
) -> ProyectoOut:
    """
    Crea un nuevo proyecto y asigna al creador como administrador.
    """
    user_id = get_current_user_id(credentials.credentials)

    insert_prj = """
        INSERT INTO Proyecto (nombre_proyecto, descripcion_proyecto, id_usuario)
        VALUES (%s, %s, %s);
    """

    new_id = execute_query(
        insert_prj,
        (proyecto_in.nombre_proyecto, proyecto_in.descripcion_proyecto, user_id),
        commit=True,
        return_lastrowid=True
    )

    if new_id is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el proyecto")

    assign_admin = """
        INSERT INTO Usuario_Proyecto (id_usuario, id_proyecto, rol_usuario_proyecto)
        VALUES (%s, %s, 'admin');
    """
    execute_query(assign_admin, (user_id, new_id), commit=True)

    created = _fetch_project_by_id(new_id)
    return ProyectoOut(**created)


@router.get(
    "/all",
    response_model=List[ProyectoOut],
    summary="Listado público de todos los proyectos"
)
def list_all_projects() -> List[ProyectoOut]:
    """
    Devuelve todos los proyectos (sin necesidad de autenticación).
    """
    query = """
        SELECT id_proyecto, nombre_proyecto, descripcion_proyecto, id_usuario
        FROM Proyecto;
    """
    rows = execute_query(query, fetchall=True) or []
    return [ProyectoOut(**r) for r in rows]

@router.get(
    "/",
    response_model=List[ProyectoOut],
    summary="Proyectos del usuario autenticado"
)
def list_my_projects(
    credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())
) -> List[ProyectoOut]:
    """
    Obtiene los proyectos en los que participa el usuario (owner o miembro).
    """
    user_id = get_current_user_id(credentials.credentials)
    query = "SELECT id_proyecto FROM Usuario_Proyecto WHERE id_usuario = %s"
    project_ids = [row["id_proyecto"] for row in (execute_query(query, (user_id,), fetchall=True) or [])]

    if not project_ids:
        return []

    placeholders = ','.join(['%s'] * len(project_ids))
    query = f"SELECT id_proyecto, nombre_proyecto, descripcion_proyecto, id_usuario FROM Proyecto WHERE id_proyecto IN ({placeholders})"
    projects = execute_query(query, tuple(project_ids), fetchall=True) or []

    for project in projects:
        project.update(_get_project_with_users(project["id_proyecto"]))

    return projects


@router.get(
    "/{id_proyecto}",
    response_model=ProyectoOut,
    dependencies=[Depends(BearerJWT())],
    summary="Detalles de un proyecto con control de acceso"
)
def get_project(
    id_proyecto: int,
    credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())
) -> ProyectoOut:
    """
    Obtiene un proyecto por ID solo si el usuario es owner o miembro.
    """
    user_id = get_current_user_id(credentials.credentials)
    query = """
    SELECT id_proyecto FROM Proyecto
    WHERE id_proyecto = %s AND (id_usuario = %s OR EXISTS (
        SELECT 1 FROM Usuario_Proyecto WHERE id_proyecto = %s AND id_usuario = %s))
    """
    result = execute_query(query, (id_proyecto, user_id, id_proyecto, user_id), fetchone=True)
    if not result:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return _get_project_with_users(id_proyecto)

@router.patch(
    "/{id_proyecto}",
    summary="Actualiza datos de un proyecto (solo owner)"
)
def update_project(
    id_proyecto: int,
    proyecto_in: ProyectoUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())
):
    """
    Actualiza nombre o descripción de un proyecto. Solo lo puede hacer el owner.
    """
    user_id = get_current_user_id(credentials.credentials)
    _assert_owner(id_proyecto, user_id)
    
    updates, params = [], []
    if proyecto_in.nombre_proyecto is not None:
        updates.append("nombre_proyecto = %s")
        params.append(proyecto_in.nombre_proyecto)
    if proyecto_in.descripcion_proyecto is not None:
        updates.append("descripcion_proyecto = %s")
        params.append(proyecto_in.descripcion_proyecto)

    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay campos para actualizar")

    params.extend([id_proyecto, user_id])
    query = f"""
        UPDATE Proyecto
        SET {', '.join(updates)}
        WHERE id_proyecto = %s AND id_usuario = %s;
    """
    execute_query(query, tuple(params), commit=True)
    return {"message": "Proyecto actualizado exitosamente"}

@router.delete(
    "/{id_proyecto}",
    summary="Elimina un proyecto (solo owner)"
)
def delete_project(
    id_proyecto: int,
    credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())
):
    """
    Elimina un proyecto si el usuario autenticado es su owner.
    """
    user_id = get_current_user_id(credentials.credentials)
    _assert_owner(id_proyecto, user_id)

    query = "DELETE FROM Proyecto WHERE id_proyecto = %s AND id_usuario = %s;"
    execute_query(query, (id_proyecto, user_id), commit=True)
    return {"message": "Proyecto eliminado exitosamente"}
