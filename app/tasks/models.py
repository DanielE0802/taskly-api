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

class TareaCreate(TareaBase):
    pass

class TareaUpdate(BaseModel):
    titulo_tarea: Optional[str]
    descripcion_tarea: Optional[str]
    estado_tarea: Optional[str]
    fecha_limite_tarea: datetime

class TareaOut(TareaBase):
    id_tarea: int
    id_usuario: int
    id_proyecto: int

    class Config:
        from_attributes = True
