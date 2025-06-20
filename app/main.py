from fastapi import FastAPI, Body
from auth.routes import router as auth_router
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Routers
from tasks.routes import task_router
from projects.routes import router as project_router
from tasks.task_by_project_routes import router as task_by_project_router
from users.routes import users_router
from auth.utils import BearerJWT
from fastapi import Depends
from utils.email import send_reset_email
from utils.limiter import limiter
from fastapi import Request
from fastapi.responses import PlainTextResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(
    title="Taskly API",
    description="API for Taskly, a task management application.",
    version = "0.1.0"
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return PlainTextResponse("Demasiadas peticiones. Inténtalo más tarde.", status_code=429)

app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

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


