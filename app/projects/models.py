from pydantic import BaseModel
from typing import Optional, List

class ProyectoBase(BaseModel):
    nombre_proyecto: str
    descripcion_proyecto: str

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(BaseModel):
    nombre_proyecto: str | None = None
    descripcion_proyecto: str | None = None

class UsuarioProyectoOut(BaseModel):
    id_usuario: int
    nombre_usuario: str
    rol_usuario_proyecto: str
    

class Proyecto(BaseModel):
    id_proyecto: Optional[int]
    nombre_proyecto: str
    descripcion_proyecto: Optional[str]
    id_usuario: int
    usuarios: List[UsuarioProyectoOut] = []

class UsuarioProyectoCreate(BaseModel):
    id_usuario: int
    rol_usuario_proyecto: str
    
