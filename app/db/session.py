from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings, settingsReadOnly

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

engineReadOnly = create_engine(settingsReadOnly.DATABASE_RO_URL, pool_pre_ping=True)
SessionLocalRo = sessionmaker(
    autocommit=False, autoflush=False, bind=engineReadOnly, future=True
)
