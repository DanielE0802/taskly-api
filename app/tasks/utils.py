from fastapi import HTTPException, status
from database import execute_query
from typing import Dict, Any

def check_user_in_project(id_proyecto: int, user_id: int):
    """Verifica si el usuario tiene acceso al proyecto."""
    query = "SELECT * FROM Usuario_Proyecto WHERE id_proyecto = %s AND id_usuario = %s"
    result = execute_query(query, (id_proyecto, user_id), fetchone=True)
    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes acceso a este proyecto")


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