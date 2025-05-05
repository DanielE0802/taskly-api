from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str
    id: int

    class Config:
        orm_mode = True  # Esto permite que Pydantic se use con SQLAlchemy

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class CreateTask(BaseModel):
    title: str = Field(min_length=5, max_length=20, default="Tarea 1")
    description: str = Field(min_length=5, max_length=50, default="Tengo que hacer tal cosa")
    completed: bool
    created_by: str = Field(min_length=5, max_length=20)

class GetTask(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    completed: bool
    created_by: str
