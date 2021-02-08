from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from app.db import Base

class RegisteredUser(Base):

    __tablename__ = "registered_users"

    uuid = Column(Integer, primary_key=True)
    blocked = Column(Boolean, nullable=False)
    email = Column(String(60), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, email):
        self.email = email
        self.blocked = False
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def serialize(self):
        return {
            "uuid": self.uuid,
            "email": self.email,
            "blocked": self.blocked,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def is_bloked(self):
        return self.blocked

    def block(self):
        self.blocked = True

    def unblock(self):
        self.blocked = False