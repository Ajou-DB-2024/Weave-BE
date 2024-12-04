from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URL: str

    PORT: int

    TOKEN_SECRET: str
    TOKEN_ALGORITHM: str

    PY_ENV: str

    class Config:
        env_file = ".env"

settings = Settings()
