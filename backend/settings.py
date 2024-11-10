from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    finance_database_url: str = 'sqlite+aiosqlite:///:memory:'
    test_database_url: str = 'sqlite+aiosqlite:///:memory:'
    echo_sql: bool = False
    echo_test_sql: bool = True
    test: bool = False

    project_name: str = "Ebanx Home Assignment"
    project_description: str = "Home Assignment for Software Engineer at Ebanx"
    project_version: str = "0.0.1"


settings = Settings()
