from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
import uuid
import jwt
from datetime import datetime, timedelta
from database import execute_query, execute_update
from auth.utils import hash_password, verify_password, create_access_token

router = APIRouter()

# Ruta de registro de usuario
@router.post("/register")
def register_user(username: str, email: str, password: str):
    # Verificar si el usuario ya existe
    query = "SELECT * FROM users WHERE username = %s"
    existing_user = execute_query(query, (username,))
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Generar un UUID para el usuario
    id = str(uuid.uuid4())

    # Hashear la contraseña
    hashed_password = hash_password(password)

    # Insertar el usuario en la base de datos
    query = "INSERT INTO users (id, username, email, hashed_password) VALUES (%s, %s, %s, %s)"
    try:
        execute_update(query, (id, username, email, hashed_password))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "User registered successfully"}

# Ruta de login
@router.post("/login")
def login_for_access_token(username: str, password: str):
    # Buscar el usuario en la base de datos
    query = "SELECT * FROM users WHERE username = %s"
    user = execute_query(query, (username,))

    if not user or not verify_password(password, user[0]["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Crear el token JWT
    access_token = create_access_token(data={"sub": user[0]["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
