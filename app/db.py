from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import config


engine = create_async_engine(config.POSTGRES_DSN, echo=True)


AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

from sqlalchemy.orm import declarative_base
Base = declarative_base()
