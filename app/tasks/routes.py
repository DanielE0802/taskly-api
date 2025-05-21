from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from auth import schemas , utils
from auth.utils import BearerJWT, get_current_user_id
from fastapi import APIRouter, HTTPException
from database import execute_query, execute_update
import auth.models as models
from tasks.models import TareaCreate, TareaOut, TareaUpdate

task_router = APIRouter()


@task_router.get("", dependencies=[Depends(utils.BearerJWT())])
def get_all_tasks(credentials: HTTPAuthorizationCredentials = Depends(utils.BearerJWT())):
    # get bearer token for authentication and get all tasks by user
    user_id = utils.get_current_user_id(credentials.credentials)
    print(user_id)
    query = "SELECT * FROM Tarea WHERE id_usuario = %s"
    tasks = execute_query(query, (user_id,))
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return {"tasks": tasks}


# Ruta para obtener todas las tareas de un usuario
@task_router.get("/{id}", dependencies=[Depends(utils.BearerJWT())])
def get_tasks(id: str):
    query = "SELECT * FROM tasks WHERE id = %s"
    tasks = execute_query(query, (id,))
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return {"tasks": tasks}

# Ruta para crear una tarea
@task_router.post("/", dependencies=[Depends(utils.BearerJWT())])
def create_task(data: models.Tarea, credentials: HTTPAuthorizationCredentials = Depends(utils.BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    query = """
        INSERT INTO Tarea (titulo_tarea, descripcion_tarea, estado_tarea, fecha_limite_tarea, id_proyecto, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        execute_update(query, (data.titulo_tarea, data.descripcion_tarea, data.estado_tarea, data.fecha_limite_tarea, data.id_proyecto, user_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Task created successfully"}


# Task_By_Projects


def check_user_in_project(id_proyecto: int, user_id: int):
    query = "SELECT * FROM usuario_proyecto WHERE id_proyecto = %s AND id_usuario = %s"
    result = execute_query(query, (id_proyecto, user_id), fetchone=True)
    if not result:
        raise HTTPException(status_code=403, detail="No tienes acceso a este proyecto")

@task_router.get("/proyecto/{id_proyecto}", response_model=list[TareaOut])
def get_tareas_by_project(id_proyecto: int, credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    check_user_in_project(id_proyecto, user_id)

    query = "SELECT * FROM tarea WHERE id_proyecto = %s"
    tareas = execute_query(query, (id_proyecto,), fetchall=True)
    return tareas

@task_router.post("/proyecto/{id_proyecto}", response_model=TareaOut)
def create_tarea(id_proyecto: int, tarea: TareaCreate, credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    check_user_in_project(id_proyecto, user_id)

    query = """
    INSERT INTO tarea (titulo_tarea, descripcion_tarea, estado_tarea, fecha_limite_tarea, id_proyecto, id_usuario)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (tarea.titulo_tarea, tarea.descripcion_tarea, tarea.estado_tarea, tarea.fecha_limite_tarea, id_proyecto, user_id)
    tarea_id = execute_query(query, params, commit=True, fetch_lastrowid=True)

    query = "SELECT * FROM tarea WHERE id_tarea = %s"
    return execute_query(query, (tarea_id,), fetchone=True)

@task_router.get("/{id_tarea}", response_model=TareaOut)
def get_tarea(id_tarea: int, credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    query = "SELECT * FROM tarea WHERE id_tarea = %s"
    tarea = execute_query(query, (id_tarea,), fetchone=True)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    check_user_in_project(tarea["id_proyecto"], user_id)
    return tarea

@task_router.patch("/{id_tarea}")
def update_tarea(id_tarea: int, tarea: TareaUpdate, credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    query = "SELECT * FROM tarea WHERE id_tarea = %s"
    tarea_db = execute_query(query, (id_tarea,), fetchone=True)
    if not tarea_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    check_user_in_project(tarea_db["id_proyecto"], user_id)

    updates = []
    params = []
    for field, value in tarea.dict(exclude_unset=True).items():
        updates.append(f"{field} = %s")
        params.append(value)
    if not updates:
        raise HTTPException(status_code=400, detail="Nada que actualizar")
    query = f"UPDATE tarea SET {', '.join(updates)} WHERE id_tarea = %s"
    params.append(id_tarea)
    execute_query(query, tuple(params), commit=True)
    return {"message": "Tarea actualizada"}

@task_router.delete("/{id_tarea}")
def delete_tarea(id_tarea: int, credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    query = "SELECT * FROM tarea WHERE id_tarea = %s"
    tarea = execute_query(query, (id_tarea,), fetchone=True)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    check_user_in_project(tarea["id_proyecto"], user_id)

    query = "DELETE FROM tarea WHERE id_tarea = %s"
    execute_query(query, (id_tarea,), commit=True)
    return {"message": "Tarea eliminada correctamente"}