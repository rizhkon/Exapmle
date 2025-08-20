import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    POSTGRES_PORT: int = os.environ.get("POSTGRES_PORT")
    MINIO_BACK_HOST: str = os.environ.get("MINIO_BACK_HOST")
    BUCKET_FOR_COPY: str = os.environ.get("BUCKET_FOR_COPY")
    ES_HOST: str = os.environ.get("ES_HOST")
    ES_PORT: int = os.environ.get("ES_PORT")
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT: int = 6379
    AUTH_URL: str = os.environ.get("AUTH_URL")
    MINIO_SECRET_KEY: str = os.environ.get("MINIO_SECRET_KEY")
    NIFI_SECRET_KEY: str = os.environ.get("NIFI_SECRET_KEY")
    OTHER_SERVICE_SECRET_KEY: str = os.environ.get("OTHER_SERVICE_SECRET_KEY")
    REDIS_PASSWORD: str = os.environ.get("REDIS_PASSWORD")
    FTP_SECRET_KEY: str = os.environ.get("FTP_SECRET_KEY")
    REQUEST_MINIO_SECRET: str = os.environ.get("REQUEST_MINIO_SECRET")
    BUCKET_FOR_UPLOAD: str = os.environ.get("BUCKET_FOR_UPLOAD")
    PLICANTE_API: str = os.environ.get("PLICANTE_API")
    PLICANTE_API_KEY: str = os.environ.get("PLICANTE_API_KEY")
    STYLE_DIR: str = os.environ.get("STYLE_DIR")
    MOCKUP_DIR: str = os.environ.get("MOCKUP_DIR")
    PROJECTION_DIR: str = os.environ.get("PROJECTION_DIR")
    TEMP_DIR_PATH: str = os.environ.get("TEMP_DIR_PATH")

settings = Settings()

