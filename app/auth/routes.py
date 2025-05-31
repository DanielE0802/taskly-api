from fastapi import APIRouter, HTTPException, Depends, status
from database import execute_query, execute_update
from auth.utils import hash_password, verify_password, create_access_token
from auth import models

router = APIRouter()

# Ruta de registro de usuario
@router.post("/register")
def register_user(user: models.UserRegister):
    """Registra un nuevo usuario en la base de datos."""
    query = "SELECT * FROM Usuario WHERE correo_usuario = %s"
    existing_user = execute_query(query, (user.correo_usuario,))
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Verificar si el nombre de usuario ya existe
    query = "SELECT * FROM Usuario WHERE nombre_usuario = %s"
    existing_user = execute_query(query, (user.nombre_usuario,))
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hashear la contraseña
    hashed_password = hash_password(user.clave_usuario)

    # Insertar el usuario en la base de datos
    query = "INSERT INTO Usuario (id_usuario, nombre_usuario, correo_usuario, clave_usuario) VALUES (%s, %s, %s, %s)"
    try:
        execute_update(query, (None, user.nombre_usuario, user.correo_usuario, hashed_password))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "User registered successfully"}

# Ruta de login
@router.post("/login")
def login_for_access_token(user: models.UserLogin) -> models.Token:
    """Inicia sesión y devuelve un token de acceso."""
    query = "SELECT * FROM Usuario WHERE correo_usuario = %s"
    db_user = execute_query(query, (user.correo_usuario,), fetchone=True)
    if not db_user or not verify_password(user.clave_usuario, db_user['clave_usuario']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": db_user["correo_usuario"]})
    return models.Token(access_token=token, token_type="bearer")

