from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import settings as s


sql_link = (
    f"postgresql+asyncpg://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@{s.POSTGRES_SERVER}"
    f":{s.POSTGRES_PORT}/{s.POSTGRES_DB}"
)
engine = create_async_engine(sql_link, echo=False, poolclass=NullPool)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, class_=AsyncSession, bind=engine
)
