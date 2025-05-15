from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
import uuid
import jwt
from datetime import datetime, timedelta
from database import execute_query, execute_update

router = APIRouter()

# Configuración de seguridad
SECRET_KEY = "mysecretkey"  # Cambia esto por una clave secreta más segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Crear un objeto CryptContext para manejar el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear la contraseña
def hash_password(password: str):
    return pwd_context.hash(password)

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Función para generar el JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Ruta de registro de usuario
@router.post("/register")
def register_user(username: str, email: str, password: str):
    # Verificar si el usuario ya existe
    query = "SELECT * FROM users WHERE username = %s"
    existing_user = execute_query(query, (username,))
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Generar un UUID para el usuario
    user_id = str(uuid.uuid4())

    # Hashear la contraseña
    hashed_password = hash_password(password)

    # Insertar el usuario en la base de datos
    query = "INSERT INTO users (id, username, email, hashed_password) VALUES (%s, %s, %s, %s)"
    try:
        execute_update(query, (user_id, username, email, hashed_password))
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
