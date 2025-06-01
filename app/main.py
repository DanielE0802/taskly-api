from fastapi import FastAPI, Body
from auth.routes import router as auth_router
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

# Routers
from tasks.routes import task_router
from projects.routes import router as project_router
from tasks.task_by_project_routes import router as task_by_project_router
from users.routes import users_router
from auth.utils import BearerJWT
from fastapi import Depends

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

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"], dependencies=[Depends(BearerJWT())])
app.include_router(project_router, prefix="/projects", tags=["Projects"], dependencies=[Depends(BearerJWT())])
app.include_router(task_by_project_router, prefix="/tasks", tags=["Tasks By Projects"], dependencies=[Depends(BearerJWT())])
app.include_router(users_router, prefix="/users", tags=["Users"], dependencies=[Depends(BearerJWT())])

@app.get("/")
def read_root():
    """
    Root endpoint that redirects to the documentation.
    """
    return RedirectResponse(url="/docs")


