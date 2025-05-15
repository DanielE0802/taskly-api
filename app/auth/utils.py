from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

# Cargar la clave secreta desde las variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Verificación del token JWT
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Token verification failed: {str(e)}")