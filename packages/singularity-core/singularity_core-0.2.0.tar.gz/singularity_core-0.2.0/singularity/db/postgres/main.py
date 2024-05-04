from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from singularity.config import POSTGRES_ASYNC_PREFIX, POSTGRES_URI

DATABASE_URI = POSTGRES_URI
DATABASE_PREFIX = POSTGRES_ASYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)

async_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
