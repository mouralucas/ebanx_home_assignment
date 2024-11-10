from fastapi import FastAPI

from backend.settings import settings
from routes import account
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.project_version,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url="/",
    redoc_url="/redoc",
)

@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(content=0, status_code=404)
    return await app.default_exception_handler(request, exc)

app.include_router(account.router)
