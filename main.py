from fastapi import FastAPI
from starlette import status

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
    """
    Custom 404 exception handler to suit the required output with integer 0
    :param request:
    :param exc:
    :return:
    """
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return JSONResponse(content=0, status_code=status.HTTP_404_NOT_FOUND)
    return await app.default_exception_handler(request, exc)

app.include_router(account.router)
