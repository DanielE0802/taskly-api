from fastapi import APIRouter, HTTPException, Query, status
from database import execute_query
from users.models import User

users_router = APIRouter()

@users_router.get("/users", response_model=list[User])
def get_users_from_project(id_proyecto: int):
    """
    Obtiene los usuarios asociados a un proyecto específico.
    """
    query = """
    SELECT u.id_usuario, u.nombre_usuario
    FROM Usuario u
    JOIN Usuario_Proyecto up ON u.id_usuario = up.id_usuario
    WHERE up.id_proyecto = %s;
    """
    rows = execute_query(query, (id_proyecto,), fetchall=True)
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found for this project")
    users = [User(id_usuario=row["id_usuario"], nombre_usuario=row["nombre_usuario"]) for row in rows]
    return users

@users_router.get("/users/{id_usuario}", response_model=User)
def get_user_by_id(id_usuario: int):
    """
    Obtiene un usuario por su ID y devuelve su nombre y proyectos asociados.
    """
    query = """
    SELECT
        u.id_usuario,
        u.nombre_usuario,
        GROUP_CONCAT(p.nombre_proyecto) AS proyectos
    FROM Usuario u
    LEFT JOIN Usuario_Proyecto up ON u.id_usuario = up.id_usuario
    LEFT JOIN Proyecto p ON up.id_proyecto = p.id_proyecto
    WHERE u.id_usuario = %s
    GROUP BY u.id_usuario;
    """
    row = execute_query(query, (id_usuario,), fetchone=True)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Convertir el string de proyectos a lista (puede ser None)
    proyectos = row["proyectos"].split(",") if row["proyectos"] else []
    return User(id_usuario=row["id_usuario"], nombre_usuario=row["nombre_usuario"], proyectos=proyectos)

@users_router.get("/users/search", response_model=list[User])
def search_users(name: str = Query(..., description="Nombre del usuario a buscar")):
    """
    Busca usuarios por nombre.
    """
    query = "SELECT id_usuario, nombre_usuario FROM Usuario WHERE nombre_usuario ILIKE %s;"
    rows = execute_query(query, (f"%{name}%",), fetchall=True)
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    users = [User(id_usuario=row["id_usuario"], nombre_usuario=row["nombre_usuario"]) for row in rows]
    return users

@users_router.post("/users", response_model=User)
def asign_user_to_project(id_proyecto: int, id_usuario: int):
    """
    Asigna un usuario a un proyecto.
    """
    query = "SELECT id_usuario FROM Usuario_Proyecto WHERE id_proyecto = %s AND id_usuario = %s;"
    existing_user = execute_query(query, (id_proyecto, id_usuario), fetchone=True)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already assigned to this project")
    
    query = "SELECT id_usuario FROM Usuario WHERE id_usuario = %s;"
    user_exists = execute_query(query, (id_usuario,), fetchone=True)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Check if the project exists
    query = "SELECT id_proyecto FROM Proyecto WHERE id_proyecto = %s;"
    project_exists = execute_query(query, (id_proyecto,), fetchone=True)
    if not project_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    query = "INSERT INTO Usuario_Proyecto (id_proyecto, id_usuario, rol_usuario_proyecto) VALUES (%s, %s, 'miembro');"
    execute_query(query, (id_proyecto, id_usuario), commit=True)
    return {"message": "User assigned to project successfully"}