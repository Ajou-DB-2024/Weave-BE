from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    HOST: str
    PORT: int

    PY_ENV: str

    class Config:
        env_file = ".env"

settings = Settings()
