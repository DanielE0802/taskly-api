from fastapi import HTTPException, status
from database import execute_query

def check_user_in_project(id_proyecto: int, user_id: int):
    """Verifica si el usuario tiene acceso al proyecto."""
    query = "SELECT * FROM Usuario_Proyecto WHERE id_proyecto = %s AND id_usuario = %s"
    result = execute_query(query, (id_proyecto, user_id), fetchone=True)
    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes acceso a este proyecto")
