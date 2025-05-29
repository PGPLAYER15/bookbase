from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Configuración para PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Muestra queries en consola (solo desarrollo)
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# Sesión para interactuar con la DB
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

from typing import AsyncGenerator

# Función para obtener sesión (usada en dependencias)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session