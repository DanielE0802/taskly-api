from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from app.auth import schemas
from app.database import SessionLocal
from app.jwt.utils import validate_token
from app.auth.models import Task as TaskModel

task_router = APIRouter()

#TODO: mover esto a un archivo de configuracion
class BearerJWT(HTTPBearer):
    """Custom HTTPBearer class to handle JWT authentication."""
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        auth = await super().__call__(request)
        if not auth or not isinstance(auth.credentials, str):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Don't have credentials")
        credentials: HTTPAuthorizationCredentials = HTTPAuthorizationCredentials(scheme=auth.scheme, credentials=auth.credentials)
        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Don't have credentials")
        
        validate_token(credentials.credentials)
        return credentials


@task_router.post("", dependencies=[Depends(BearerJWT())])
def create_task(task: schemas.CreateTask):
    db = SessionLocal()
    new_task = TaskModel(**task.model_dump())
    db.add(new_task)
    db.commit()
    return JSONResponse(content={
        'message': 'se ha creado correctamente la tarea ' + task.title,
        'tarea': task.model_dump()
    }, status_code=201)


@task_router.get("", tags=["tasks"], dependencies=[Depends(BearerJWT())])
def get_tasks():
    db = SessionLocal()
    data = db.query(TaskModel).all()
    return JSONResponse(content={
        'message': 'se han encontrado las tareas',
        'tareas': jsonable_encoder(data)
    }, status_code=status.HTTP_200_OK)

@task_router.get("/", tags=["tasks"], dependencies=[Depends(BearerJWT())])
def get_tasks_by_author(created_by: str = Query(min_length=3, max_length=20)):
    db = SessionLocal()
    data = db.query(TaskModel).filter(TaskModel.created_by == created_by).all()
    if not data:
        return JSONResponse(content={
            'message': 'no se han encontrado tareas',
            'tareas': None
        }, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content={
        'message': 'se han encontrado las tareas',
        'tareas': jsonable_encoder(data)
    }, status_code=status.HTTP_200_OK)


@task_router.get("/tasks/{task_id}", tags=["tasks"], dependencies=[Depends(BearerJWT())])
def get_task_by_id(task_id: int):
    db = SessionLocal()
    data = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not data:
        return JSONResponse(content={
            'message': 'no se ha encontrado la tarea',
            'tarea': None
        }, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content={
        'message': 'se ha encontrado la tarea',
        'tarea': jsonable_encoder(data)
    }, status_code=status.HTTP_200_OK)
    
@task_router.put("/tasks/{task_id}", tags=["tasks"], dependencies=[Depends(BearerJWT())])
def update_task(task_id: int, task: schemas.CreateTask):
    db= SessionLocal()
    data= db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not data:
        return JSONResponse(content={
            'message': 'no se ha encontrado la tarea',
            'tarea': None
        }, status_code=status.HTTP_404_NOT_FOUND)
    
    db.query(TaskModel).filter(TaskModel.id == task_id).update({
        TaskModel.title: task.title,
        TaskModel.description: task.description,
        TaskModel.completed: task.completed,
        TaskModel.created_by: task.created_by
    })
    db.commit()
    data = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    return JSONResponse(content={
        'message': 'se ha actualizado la tarea',
        'tarea': jsonable_encoder(data)
    }, status_code=status.HTTP_200_OK)

@task_router.delete("/tasks/{task_id}", tags=["tasks"], dependencies=[Depends(BearerJWT())])
def delete_task(task_id: int):
    db = SessionLocal()
    data = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not data:
        return JSONResponse(content={
            'message': 'no se ha encontrado la tarea',
            'tarea': None
        }, status_code=status.HTTP_404_NOT_FOUND)
    
    db.delete(data)
    db.commit()
    return JSONResponse(content={
        'message': 'se ha eliminado la tarea',
        'tarea': jsonable_encoder(data)
    }, status_code=status.HTTP_200_OK)
