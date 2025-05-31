from pydantic import BaseModel
from typing import Optional
from typing import List

class Usuario(BaseModel):
    """
    Modelo para representar un usuario en el sistema.
    Contiene información básica del usuario como ID, nombre, correo y clave.
    """
    id_usuario: Optional[int]
    nombre_usuario: Optional[str]
    correo_usuario: str
    clave_usuario: str

class UserRegister(BaseModel):
    """
    Modelo para el registro de un nuevo usuario.
    """
    nombre_usuario: str
    correo_usuario: str
    clave_usuario: str

class UserLogin(BaseModel):
    """
    Modelo para el inicio de sesión de un usuario.
    """
    correo_usuario: str
    clave_usuario: str

class Token(BaseModel):
    """
    Modelo para el token de acceso.
    """
    access_token: str
    token_type: str = "bearer"
