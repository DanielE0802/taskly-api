from fastapi import FastAPI, Body
from auth.routes import router as auth_router
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

# Routers
from tasks.routes import task_router
from projects.routes import router as project_router
from tasks.task_by_project_routes import router as task_by_project_router

app = FastAPI(
    title="Taskly API",
    description="API for Taskly, a task management application.",
    version = "0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(project_router, prefix="/projects", tags=["projects"])
app.include_router(task_by_project_router, prefix="/tasks", tags=["tasks by projects"])

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


