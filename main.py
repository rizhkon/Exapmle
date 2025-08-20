import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.setup_logger import setup_logger

from src.api.routers import role2_file_type_routers

from src.middleware import (
    CatchExceptionsMiddleware,
    LoggingMiddleware,
)


os.environ["TZ"] = "Europe/Moscow"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await setup_logger()
    yield


app = FastAPI(
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(CatchExceptionsMiddleware)

app.add_middleware(LoggingMiddleware)
app.include_router(role2_file_type_routers.router)
