from pydantic import BaseModel, field_serializer

class User(BaseModel):
    id_usuario: int
    nombre_usuario: str
    proyectos: list[str] = []

    @field_serializer("id_usuario")
    def serialize_id(self, value: int) -> str:
        return str(value)

    @field_serializer("nombre_usuario")
    def serialize_name(self, value: str) -> str:
        return value.strip().title()