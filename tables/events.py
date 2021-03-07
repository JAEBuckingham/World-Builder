"""events table"""
from sqlalchemy import Column, Integer, String

from tables.base import Base


class Events(Base):
    """events table"""
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f'<User(id={self.id}, name={self.name})>'
