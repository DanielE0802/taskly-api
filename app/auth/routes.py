from fastapi import APIRouter, HTTPException, Depends, status
from database import execute_query, execute_update
from auth.utils import hash_password, verify_password, create_access_token
from utils.email import send_reset_email
from utils.reset_tokens import generate_reset_code
from auth import models
from datetime import datetime, timedelta
from slowapi.errors import RateLimitExceeded
from utils.limiter import limiter
from fastapi import Request

router = APIRouter()

# Ruta de registro de usuario
@router.post("/register")
async def register_user(user: models.UserRegister):
    """Registra un nuevo usuario en la base de datos."""
    query = "SELECT * FROM Usuario WHERE correo_usuario = %s"
    existing_user = execute_query(query, (user.correo_usuario,), fetchone=True)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hashear la contraseña
    hashed_password = hash_password(user.clave_usuario)

    # Insertar el usuario en la base de datos
    query = "INSERT INTO Usuario (id_usuario, nombre_usuario, correo_usuario, clave_usuario) VALUES (%s, %s, %s, %s)"
    try:
        execute_update(query, (None, user.nombre, user.correo_usuario, hashed_password))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    try:
        await send_reset_email(user.correo_usuario,'welcome_template.html', {"nombre": user.nombre} , subject="Registro exitoso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending welcome email: {str(e)}")

    return {"message": "User registered successfully"}

# Ruta de login
@router.post("/login")
def login_for_access_token(user: models.UserLogin) -> models.Token:
    """Inicia sesión y devuelve un token de acceso."""
    query = "SELECT * FROM Usuario WHERE correo_usuario = %s"
    db_user = execute_query(query, (user.correo_usuario,), fetchone=True)
    if not db_user or not verify_password(user.clave_usuario, db_user['clave_usuario']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"email": db_user["correo_usuario"], "username": db_user["nombre_usuario"]})
    return models.Token(access_token=token, token_type="bearer")


@router.post("/send-code")
@limiter.limit("5/minute")
async def send_reset_code(data: models.ResetPasswordRequest, request: Request):
    """Envía un código de restablecimiento de contraseña al correo del usuario."""
    user = execute_query("SELECT id_usuario FROM Usuario WHERE correo_usuario = %s", (data.correo_usuario,), fetchone=True)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    code = generate_reset_code()
    expiry = datetime.utcnow() + timedelta(minutes=15)

    execute_update(
        "UPDATE Usuario SET reset_token = %s, reset_token_expiry = %s WHERE correo_usuario = %s",
        (code, expiry, data.correo_usuario)
    )

    await send_reset_email(data.correo_usuario, code, 'reset_password_email.html', {"code": code}, subject="Restablecimiento de contraseña")
    return {"message": "Código enviado al correo"}

@router.post("/reset-password")
def reset_password(data: models.ResetConfirm):
    user = execute_query(
        "SELECT id_usuario, reset_token, reset_token_expiry FROM Usuario WHERE correo_usuario = %s",
        (data.email,), fetchone=True
    )
    if not user or user["reset_token"] != data.code:
        raise HTTPException(status_code=400, detail="Código inválido")
    
    if datetime.utcnow() > user["reset_token_expiry"]:
        raise HTTPException(status_code=400, detail="El código ha expirado")
    
    password = hash_password(data.new_password)

    execute_update("UPDATE Usuario SET clave_usuario = %s, reset_token = NULL, reset_token_expiry = NULL WHERE correo_usuario = %s",
                   (password, data.email))

    return {"message": "Contraseña actualizada correctamente"}

