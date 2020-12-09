from datetime import datetime

from app.db import Base
from sqlalchemy import Column, DateTime, Integer, String


class RegisteredUser(Base):

    __tablename__ = "registered_users"

    uuid = Column(Integer, primary_key=True)
    email = Column(String(60), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, email):
        self.email = type
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def serialize(self):
        return {
            "uuid": self.uuid,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
