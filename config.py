from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "my_super_secret_key_12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()