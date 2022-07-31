from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = create_engine(settings.get_ro_db_connection, pool_pre_ping=True)
SessionLocalRo = sessionmaker(autocommit=False, autoflush=False, bind=engine)
