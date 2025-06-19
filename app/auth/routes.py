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


# @router.post("/change-password")
# def change_password(user: models.UserChangePassword, credentials: Depends(models.BearerJWT())):
#     """Cambia la contraseña del usuario autenticado."""
#     user_id = models.get_current_user_id(credentials.credentials)
    
#     query = "SELECT * FROM Usuario WHERE id_usuario = %s"
#     db_user = execute_query(query, (user_id,), fetchone=True)
    
#     if not db_user or not verify_password(user.clave_actual, db_user['clave_usuario']):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is incorrect")
    
#     # Hashear la nueva contraseña
#     hashed_new_password = hash_password(user.nueva_clave_usuario)
    
#     query = "UPDATE Usuario SET clave_usuario = %s WHERE id_usuario = %s"
#     try:
#         execute_update(query, (hashed_new_password, user_id))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
#     return {"message": "Password changed successfully"}