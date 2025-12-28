from typing import Generator
import os
from sqlmodel import SQLModel, Session, create_engine

# Render (and others) might provide 'postgres://' which SQLAlchemy 2.0+ doesn't support.
# We need to replace it with 'postgresql://'
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/workout")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator:
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
