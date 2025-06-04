from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from auth import utils
from auth.utils import BearerJWT
from fastapi import APIRouter, HTTPException
from database import execute_query
from tasks.models import TareaCreate, TareaOut
from tasks.routes import check_user_in_project

router = APIRouter()

@router.get("/proyecto/{id_proyecto}", response_model=list[TareaOut])
def get_tareas_by_project(id_proyecto: int, credentials: HTTPAuthorizationCredentials = Depends(BearerJWT())):
    user_id = utils.get_current_user_id(credentials.credentials)
    check_user_in_project(id_proyecto, user_id)

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
    WHERE t.id_proyecto = %s;
    """
    rows = execute_query(query, (id_proyecto,), fetchall=True)

    tareas = []
    if rows:
        for row in rows:
            tarea = {
                "id_tarea": row["id_tarea"],
                "titulo_tarea": row["titulo_tarea"],
                "descripcion_tarea": row["descripcion_tarea"],
                "estado_tarea": row["estado_tarea"],
                "fecha_limite_tarea": row["fecha_limite_tarea"],
                "id_proyecto": row["id_proyecto"],
                "usuario": {
                    "id_usuario": row["id_usuario"],
                    "nombre": row["nombre_usuario_creador"]
                },
                "responsable": {
                    "id_usuario": row["id_responsable"],
                    "nombre": row["nombre_usuario_responsable"]
                } if row["id_responsable"] else None
            }
            tareas.append(tarea)
    return tareas

