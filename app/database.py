from app.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(engine)

class Base(DeclarativeBase):
    pass