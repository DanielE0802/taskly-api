from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security.http import HTTPAuthorizationCredentials
from auth.utils import BearerJWT, get_current_user_id
from database import execute_query, execute_update
from tasks.models import TareaCreate, TareaOut, TareaUpdate
from tasks.utils import check_user_in_project
from typing import Optional, List, Dict, Any
task_router = APIRouter()

def build_task_response(tarea: Dict[str, Any]) -> Dict[str, Any]:
    """Construye la respuesta de una tarea con información de usuario y responsable."""
    return {
        "id_tarea": tarea["id_tarea"],
        "titulo_tarea": tarea["titulo_tarea"],
        "descripcion_tarea": tarea["descripcion_tarea"],
        "estado_tarea": tarea["estado_tarea"],
        "fecha_limite_tarea": tarea["fecha_limite_tarea"],
        "id_proyecto": tarea["id_proyecto"],
        "usuario": {
            "id_usuario": tarea["id_usuario"],
            "nombre": tarea["nombre_usuario_creador"]
        },
        "responsable": {
            "id_usuario": tarea["id_responsable"],
            "nombre": tarea["nombre_usuario_responsable"]
        } if tarea["id_responsable"] else None,
        "id_usuario": tarea["id_usuario"],
        "id_responsable": tarea["id_responsable"]
    }

@task_router.get("", response_model=List[TareaOut], dependencies=[Depends(BearerJWT())])
def get_all_tasks(
    credentials: HTTPAuthorizationCredentials = Depends(BearerJWT()),
    id_proyecto: Optional[int] = Query(None, description="Filtrar por id_proyecto")
):
    """
    Obtiene todas las tareas asociadas al usuario actual.
    Si se proporciona un id_proyecto, filtra las tareas por ese proyecto.
    """
    user_id = get_current_user_id(credentials.credentials)
    base_query = """
        SELECT
            t.id_tarea,
            t.titulo_tarea,
            t.descripcion_tarea,
            t.estado_tarea,
            t.fecha_limite_tarea,
            t.id_usuario,
            c.nombre_usuario AS nombre_usuario_creador,
            t.id_responsable,
            r.nombre_usuario AS nombre_usuario_responsable,
            t.id_proyecto
        FROM Tarea t
        LEFT JOIN Usuario c ON t.id_usuario = c.id_usuario
        LEFT JOIN Usuario r ON t.id_responsable = r.id_usuario
    """
    if id_proyecto is not None:
        query = base_query + " WHERE t.id_usuario = %s AND t.id_proyecto = %s"
        params = (user_id, id_proyecto)
    else:
        query = base_query + " WHERE t.id_usuario = %s"
        params = (user_id,)
    tareas = execute_query(query, params, fetchall=True)
    if not tareas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found")
    return {"tasks": [build_task_response(t) for t in tareas]}

@task_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(BearerJWT())])
def create_task(
    data: TareaCreate,
    credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())
):
    """
    Crea una nueva tarea en la base de datos, asociada al usuario actual y al proyecto especificado.
    """
    user_id = get_current_user_id(credentials.credentials)
    check_user_in_project(data.id_proyecto, user_id)

    query = """
        INSERT INTO tarea (titulo_tarea, descripcion_tarea, estado_tarea, fecha_limite_tarea, id_proyecto, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        execute_update(
            query,
            (
                data.titulo_tarea,
                data.descripcion_tarea,
                data.estado_tarea,
                data.fecha_limite_tarea,
                data.id_proyecto,
                user_id
            )
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"message": "Task created successfully"}

@task_router.get("/{id_tarea}", response_model=TareaOut)
def get_tarea(
    id_tarea: int,
    credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())
):
    """
    Obtiene los detalles de una tarea específica por su ID y verifica el acceso del usuario al proyecto asociado.
    """
    user_id = get_current_user_id(credentials.credentials)
    query = """
        SELECT
            t.id_tarea,
            t.titulo_tarea,
            t.descripcion_tarea,
            t.estado_tarea,
            t.fecha_limite_tarea,
            t.id_usuario,
            c.nombre_usuario AS nombre_usuario_creador,
            t.id_responsable,
            r.nombre_usuario AS nombre_usuario_responsable,
            t.id_proyecto
        FROM Tarea t
        LEFT JOIN Usuario c ON t.id_usuario = c.id_usuario
        LEFT JOIN Usuario r ON t.id_responsable = r.id_usuario
        WHERE t.id_tarea = %s
    """
    tarea = execute_query(query, (id_tarea,), fetchone=True)
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    check_user_in_project(tarea["id_proyecto"], user_id)
    return build_task_response(tarea)

@task_router.patch("/{id_tarea}")
def update_tarea(id_tarea: int, tarea: TareaUpdate, credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())):
    """Actualiza una tarea existente por su ID. Solo se actualizan los campos proporcionados en el cuerpo de la solicitud."""
    user_id = get_current_user_id(credentials.credentials)
    query = "SELECT * FROM Tarea WHERE id_tarea = %s"
    tarea_db = execute_query(query, (id_tarea,), fetchone=True)
    if not tarea_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    check_user_in_project(tarea_db["id_proyecto"], user_id)

    updates = []
    params = []
    for field, value in tarea.dict(exclude_unset=True).items():
        updates.append(f"{field} = %s")
        params.append(value)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nada que actualizar")
    query = f"UPDATE tarea SET {', '.join(updates)} WHERE id_tarea = %s"
    params.append(id_tarea)
    execute_query(query, tuple(params), commit=True)
    return {"message": f"Tarea {id_tarea} actualizada correctamente"}

@task_router.delete("/{id_tarea}")
def delete_tarea(id_tarea: int, credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())):
    """Elimina una tarea por su ID. Verifica que el usuario tenga acceso al proyecto asociado."""
    user_id = get_current_user_id(credentials.credentials)
    query = "SELECT * FROM Tarea WHERE id_tarea = %s"
    tarea = execute_query(query, (id_tarea,), fetchone=True)
    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    check_user_in_project(tarea["id_proyecto"], user_id)

    query = "DELETE FROM Tarea WHERE id_tarea = %s"
    execute_query(query, (id_tarea,), commit=True)
    return {"message": f"Tarea {id_tarea} eliminada correctamente"}