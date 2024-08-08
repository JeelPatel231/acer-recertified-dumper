from sqlalchemy import Column, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, Mapped
from sqlalchemy.types import DateTime
from datetime import datetime
import os

class Base(DeclarativeBase):
  created_at: Mapped[datetime] = Column(DateTime, default=lambda: datetime.now())

engine = create_engine(
    os.environ.get("DB_URL", "sqlite:///db.sqlite3"),
    echo = True,
)

session = Session(engine)

def init_db():
  Base.metadata.create_all(engine)
