from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "servicio_social"
    app_env: str = "development"
    app_debug: bool = True

    db_host: str = "database"
    db_port: int = 5432
    db_name: str = "serviciosocial"
    db_user: str = "serviciosocial"
    db_password: str = "serviciosocial"

    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
