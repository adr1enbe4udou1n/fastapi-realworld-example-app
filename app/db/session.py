from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings, settingsReadOnly

engine = create_async_engine(settings.DATABASE_URL.__str__(), pool_pre_ping=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

engineReadOnly = create_async_engine(settingsReadOnly.DATABASE_RO_URL.__str__(), pool_pre_ping=True)
SessionLocalRo = async_sessionmaker(autocommit=False, autoflush=False, bind=engineReadOnly, future=True)
