from fastapi import FastAPI, Body
from app.auth.routes import router as auth_router
from app.tasks.routes import task_router
from app.database import engine, Base
from fastapi.responses import RedirectResponse
app = FastAPI(
    title="Taskly API",
    description="API for Taskly, a task management application.",
    version = "0.1.0"
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])


# Crear las tablas automáticamente
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")
