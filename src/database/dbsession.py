
from __future__ import annotations
from src.settings.config import url
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from utils.logger.factory import loggers


async def create_session_pool():
    # loggers.database_session_pool('Create database engine')
    engine = create_async_engine(
        url=url
    )

    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession
    )
