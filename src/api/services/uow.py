from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from src.api.services.role2_file_type_queries import Role2FileTypeQuery
from src.database import SessionLocal



class UnitOfWork:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.role2_file_type = Role2FileTypeQuery

    async def __aenter__(self):
        self.session = self.session_factory()
        self.role2_file_type = Role2FileTypeQuery(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(SessionLocal) as uow:
        yield uow
