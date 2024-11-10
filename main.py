from fastapi import FastAPI

from backend.settings import settings
from routes import account

app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.project_version,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url="/",
    redoc_url="/redoc",
)


app.include_router(account.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
# '
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
