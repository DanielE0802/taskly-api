from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.auth import controller, models, schemas, utils
from app.database import SessionLocal
from pydantic import BaseModel
from app.jwt.utils import create_token, validate_token

router = APIRouter()

class User (BaseModel):
    email: str
    password: str

@router.post('/login')
def login(user: User):
    token: str = create_token(user.model_dump())
    return token
