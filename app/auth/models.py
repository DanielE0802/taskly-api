# from sqlalchemy import Column, Integer, String, Boolean
# from database import Base
# from datetime import datetime
# from sqlalchemy import DateTime

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(255), unique=True, index=True)
#     hashed_password = Column(String(255))
#     is_active = Column(Boolean, default=True)


# class Task(Base):
#     __tablename__ = "tasks"
    
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     title = Column(String(255), index=True)
#     description = Column(String(255))
#     completed = Column(Boolean, default=False)
#     created_by = Column(String(255))
#     created_at = Column(DateTime, default=datetime.now)
#     updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# class Proyect(Base):
#     __tablename__ = "projects"
    
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     name = Column(String(255), index=True)
#     description = Column(String(255))
#     created_by = Column(String(255))
#     created_at = Column(DateTime, default=datetime.now)
#     updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    
    
    # Modelos Pydantic para validación

from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id_usuario: Optional[int]
    nombre_usuario: Optional[str]
    correo_usuario: str
    clave_usuario: str

class Proyecto(BaseModel):
    id_proyecto: Optional[int]
    nombre_proyecto: str
    descripcion_proyecto: Optional[str]
    id_usuario: Optional[int]

class UsuarioProyecto(BaseModel):
    id_usuario_proyecto: Optional[int]
    id_usuario: int
    id_proyecto: int
    rol_usuario_proyecto: Optional[str]

class Tarea(BaseModel):
    id_tarea: Optional[int]
    titulo_tarea: str
    descripcion_tarea: Optional[str]
    estado_tarea: Optional[str]
    fecha_limite_tarea: Optional[str]
    id_proyecto: int
    id_usuario: int

class HistorialTarea(BaseModel):
    id_historial_tarea: Optional[int]
    id_tarea: int
    estado_anterior_historial_tarea: Optional[str]
    estado_nuevo_historial_tarea: str
    fecha_cambio_historial_tarea: Optional[str]
    id_usuario: int