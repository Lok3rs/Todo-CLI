from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from model.util import generate_hash

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), nullable=False)
    deadline = Column('deadline', DateTime, nullable=True)
    description = Column('description', String(250), nullable=True, default="---")
    creation_date = Column("creation_date", DateTime, nullable=False, default=datetime.utcnow)
    task_hash = Column("hash", Integer, nullable=False, default=generate_hash(name))
    done = Column("done", Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Task(name={self.name}, creation_date={self.creation_date}, task_hash={self.task_hash})>"
