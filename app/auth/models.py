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
    nombre: str
    apellido: str
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

class ResetPasswordRequest(BaseModel):
    """
    Modelo para la solicitud de restablecimiento de contraseña.
    Contiene el correo del usuario y el código de verificación.
    """
    correo_usuario: str

class validateResetCode(BaseModel):
    """
    Modelo para validar el código de restablecimiento de contraseña.
    Contiene el correo del usuario y el código de verificación.
    """
    correo_usuario: str
    code: str
class ResetConfirm(BaseModel):
    """
    Modelo para la respuesta de restablecimiento de contraseña.
    Contiene el mensaje de éxito o error.
    """
    correo_usuario: str
    code: str
    new_password: str