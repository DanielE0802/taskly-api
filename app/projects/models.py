from pydantic import BaseModel
from typing import Optional, List

class ProyectoBase(BaseModel):
    nombre_proyecto: str
    descripcion_proyecto: str
    # TODO: Añadir validación para nombre_proyecto y descripcion_proyecto
    # Por ejemplo, longitud mínima/máxima, caracteres permitidos, etc.
    # Permitir imágenes o archivos adjuntos en la descripción si es necesario
    # Considerar añadir un campo para la fecha de creación o actualización del proyecto
    # TODO:
    # fecha_creacion: Optional[str] = None
    # fecha_actualizacion: Optional[str] = None

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(BaseModel):
    nombre_proyecto: str | None = None
    descripcion_proyecto: str | None = None

class UsuarioProyectoOut(BaseModel):
    id_usuario: int
    nombre_usuario: str
    rol_usuario_proyecto: str

class ProyectoOut(BaseModel):
    id_proyecto: Optional[int]
    nombre_proyecto: str
    descripcion_proyecto: Optional[str]
    id_usuario: int
    usuarios: List[UsuarioProyectoOut] = []

class UsuarioProyectoCreate(BaseModel):
    id_usuario: int
    rol_usuario_proyecto: str

