from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime

class TareaBase(BaseModel):
    titulo_tarea: str
    descripcion_tarea: Optional[str]
    estado_tarea: Optional[str] = "pendiente"
    fecha_limite_tarea: datetime

    @field_serializer("fecha_limite_tarea")
    def serialize_fecha_limite(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

class HistorialTarea(BaseModel):
    id_historial_tarea: Optional[int]
    id_tarea: int
    estado_anterior_historial_tarea: Optional[str]
    estado_nuevo_historial_tarea: str
    fecha_cambio_historial_tarea: Optional[str]
    id_usuario: int

class UsuarioOut(BaseModel):
    id_usuario: int
    nombre: Optional[str]

class ResponsableOut(BaseModel):
    id_usuario: Optional[int] = None
    nombre: Optional[str] = None
class TareaCreate(TareaBase):
    id_usuario: int
    id_responsable: Optional[int] = None

class TareaUpdate(BaseModel):
    titulo_tarea: Optional[str] = None
    descripcion_tarea: Optional[str] = None
    estado_tarea: Optional[str] = None
    fecha_limite_tarea: Optional[datetime] = None
    id_responsable: Optional[int] = None

class TareaOut(TareaBase):
    id_tarea: int
    usuario: UsuarioOut
    responsable: Optional[ResponsableOut] = None

    class Config:
        from_attributes = True

