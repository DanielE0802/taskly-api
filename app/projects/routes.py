from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel
from auth.utils import BearerJWT
from database import execute_query, execute_update
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from auth import utils
from projects.models import Proyecto, ProyectoCreate, ProyectoUpdate, UsuarioProyectoCreate

router = APIRouter()


# Ruta para crear proyecto
@router.post("/", response_model=Proyecto, dependencies=[Depends(BearerJWT())])
def create_project(proyecto: ProyectoCreate, credentials: HTTPAuthorizationCredentials = Depends(utils.BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    if not user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear un proyecto")

    query = """
    INSERT INTO proyecto (nombre_proyecto, descripcion_proyecto, id_usuario)
    VALUES (%s, %s, %s);
    """
    
    query2 = "INSERT INTO usuario_proyecto (id_usuario, id_proyecto, rol_usuario_proyecto) VALUES (%s, %s, %s);"
    params = (proyecto.nombre_proyecto, proyecto.descripcion_proyecto, user_id)
    try:
        last_id = execute_query(query, params, commit=True, fetch_lastrowid=True)
        if not last_id:
            raise HTTPException(status_code=400, detail="Error al crear el proyecto")
        params2 = (user_id, last_id, "admin")
        execute_query(query2, params2, commit=True)
        query = "SELECT id_proyecto, nombre_proyecto, descripcion_proyecto, id_usuario FROM proyecto WHERE id_proyecto = %s;"
        created_project = execute_query(query, (last_id,), fetchone=True)
        if not created_project:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado después de la creación")

        return created_project
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear proyecto: {str(e)}")

# ruta no protegida para obtener todos los proyectos
@router.get("/all", response_model=List[Proyecto])
def get_all_projects():
    query = "SELECT id_proyecto, nombre_proyecto, descripcion_proyecto, id_usuario FROM proyecto;"
    try:
        results = execute_query(query, fetchall=True)
        if not results or results is None:
            raise HTTPException(status_code=404, detail="No se encontraron proyectos")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener proyectos: {str(e)}")

# Ruta para listar todos los proyectos de un usuario
@router.get("/", response_model=List[Proyecto], dependencies=[Depends(BearerJWT())])
def get_projects(credentials: HTTPAuthorizationCredentials = Depends(utils.BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    print(user_id)
    try:
        query = "SELECT * FROM usuario_proyecto WHERE id_usuario = %s;"
        results = execute_query(query, (user_id,), fetchall=True)
        print(results)
        if not results or results is None:
            raise HTTPException(status_code=404, detail="No se encontraron proyectos")
        project_ids = [result["id_proyecto"] for result in results]

        if not project_ids:
            return []

        # Crea una lista de placeholders del mismo tamaño que los IDs
        placeholders = ','.join(['%s'] * len(project_ids))
        query = f"SELECT id_proyecto, nombre_proyecto, descripcion_proyecto, id_usuario FROM proyecto WHERE id_proyecto IN ({placeholders});"
        projects = execute_query(query, tuple(project_ids), fetchall=True)
    

        print(project_ids)
        print(projects)
        if not projects or projects is None:
            raise HTTPException(status_code=404, detail="No se encontraron proyectos")
        
                # Por cada proyecto, trae sus usuarios
        for project in projects:
            query_users = """
            SELECT
                up.id_usuario,
                u.nombre_usuario,
                up.rol_usuario_proyecto
            FROM usuario_proyecto up
            JOIN usuario u ON up.id_usuario = u.id_usuario
            WHERE up.id_proyecto = %s;
            """
            usuarios = execute_query(query_users, (project["id_proyecto"],), fetchall=True)
            project["usuarios"] = usuarios
        
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener proyectos: {str(e)}")

# Ruta para obtener un proyecto por ID
@router.get("/{id_proyecto}", response_model=Proyecto, dependencies=[Depends(BearerJWT())])
def get_project(id_proyecto: int, credentials: HTTPAuthorizationCredentials = Depends(utils.BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    query = "SELECT id_proyecto, nombre_proyecto, descripcion_proyecto, id_usuario FROM proyecto WHERE id_proyecto = %s AND id_usuario = %s;"
    try:
        results = execute_query(query, (id_proyecto, user_id), fetchone=True)
        if not results:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener proyecto: {str(e)}")

# Ruta para actualizar un proyecto (parcial)
@router.patch("/{id_proyecto}", dependencies=[Depends(BearerJWT())])
def update_project(id_proyecto: int, proyecto: ProyectoUpdate, credentials: HTTPAuthorizationCredentials = Depends(utils.BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    fields = []
    params = []
    if proyecto.nombre_proyecto is not None:
        fields.append("nombre_proyecto = %s")
        params.append(proyecto.nombre_proyecto)
    if proyecto.descripcion_proyecto is not None:
        fields.append("descripcion_proyecto = %s")
        params.append(proyecto.descripcion_proyecto)
    if not user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar este proyecto")
    if not id_proyecto:
        raise HTTPException(status_code=400, detail="ID de proyecto no proporcionado")
    if not fields:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    
    query = f"UPDATE proyecto SET {', '.join(fields)} WHERE id_proyecto = %s AND id_usuario = %s;"
    try:
        execute_query(query, (*params, id_proyecto, user_id), commit=True)
        return {"message": "Proyecto actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar proyecto: {str(e)}")

# Ruta para eliminar un proyecto
@router.delete("/{id_proyecto}", dependencies=[Depends(BearerJWT())])
def delete_project(id_proyecto: int, credentials: HTTPAuthorizationCredentials = Depends(utils.BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    query = "DELETE FROM proyecto WHERE id_proyecto = %s AND id_usuario = %s;"
    try:
        execute_query(query, (id_proyecto, user_id))
        return {"message": "Proyecto eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar proyecto: {str(e)}")


@router.post("/{id_proyecto}/usuarios", dependencies=[Depends(BearerJWT())])
def add_user_to_project(
    id_proyecto: int,
    data: UsuarioProyectoCreate,
    credentials: HTTPAuthorizationCredentials = Depends(utils.BearerJWT())
):
    user_id = utils.get_current_user_id(credentials.credentials)
    
    # Opcional: verificar si el usuario autenticado tiene permiso para asignar usuarios
    query_check = "SELECT * FROM proyecto WHERE id_proyecto = %s AND id_usuario = %s"
    result = execute_query(query_check, (id_proyecto, user_id), fetchone=True)
    if not result:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este proyecto")

    query = """
    INSERT INTO usuario_proyecto (id_usuario, id_proyecto, rol_usuario_proyecto)
    VALUES (%s, %s, %s);
    """
    try:
        execute_update(query, (data.id_usuario, id_proyecto, data.rol_usuario_proyecto))
        return {"message": "Usuario agregado al proyecto exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar usuario al proyecto: {str(e)}")
