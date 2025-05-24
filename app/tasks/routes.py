from fastapi import APIRouter, Depends, HTTPException
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

def check_user_in_project(id_proyecto: int, user_id: int):
    query = "SELECT * FROM usuario_proyecto WHERE id_proyecto = %s AND id_usuario = %s"
    result = execute_query(query, (id_proyecto, user_id), fetchone=True)
    if not result:
        raise HTTPException(status_code=403, detail="No tienes acceso a este proyecto")


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

# Listo ✅
@task_router.get("/{id_tarea}", response_model=TareaOut)
def get_tarea(id_tarea: int, credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
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
    FROM tarea t
    LEFT JOIN usuario c ON t.id_usuario = c.id_usuario
    LEFT JOIN usuario r ON t.id_responsable = r.id_usuario
    WHERE t.id_tarea = %s"""
    print("hola")
    tarea = execute_query(query, (id_tarea,), fetchone=True)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Verificar acceso al proyecto
    check_user_in_project(tarea["id_proyecto"], user_id)
    
    result = {
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

    return result

# Listo ✅
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

# Listo ✅
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