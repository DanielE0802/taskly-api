from fastapi import HTTPException
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from database import execute_query

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cargar la clave secreta desde las variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def verify_token(token: str):
    """
    Verifica el token JWT y devuelve el payload si es válido.
    Si el token es inválido o ha expirado, lanza una excepción HTTP.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Token verification failed: {str(e)}")
    

# Función para hashear la contraseña
def hash_password(password: str)-> str:
    """
    Hashea la contraseña utilizando bcrypt.
    """
    return pwd_context.hash(password)

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña proporcionada coincide con la contraseña hasheada.
    """
    if not hashed_password:
        raise HTTPException(status_code=400, detail="Hashed password is empty")
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token de acceso JWT.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # send user id in the token
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class BearerJWT(HTTPBearer):
    """
    Custom HTTPBearer class to handle JWT authentication.
    This class overrides the __call__ method to verify the JWT token.
    """
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        auth = await super().__call__(request)
        if not auth or not isinstance(auth.credentials, str):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Don't have credentials")
        credentials: HTTPAuthorizationCredentials = HTTPAuthorizationCredentials(scheme=auth.scheme, credentials=auth.credentials)
        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Don't have credentials")
        
        verify_token(credentials.credentials)
        return credentials
    
def get_current_user_id(token: str):
    """
    Obtiene el ID del usuario actual a partir del token JWT.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    query = "SELECT id_usuario FROM Usuario WHERE correo_usuario = %s"
    result = execute_query(query, (payload.get("sub"),), fetchone=True)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = result["id_usuario"]
    return user_id