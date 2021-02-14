import os

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy import event
from app.db import Base, get_db
from app.errors.http_error import NotFoundError


class RegisteredUser(Base):

    __tablename__ = "registered_users"

    uuid = Column(Integer, primary_key=True)
    blocked = Column(Boolean, nullable=False)
    email = Column(String(60), nullable=False)
    is_admin = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, email, is_admin):
        self.email = email
        self.blocked = False
        self.is_admin = is_admin
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

    def is_blocked(self):
        return self.blocked

    def block(self):
        self.blocked = True

    def unblock(self):
        self.blocked = False


def insert_initial_values(*args, **kwargs):
    db = next(get_db())
    db.add(RegisteredUser(email=os.getenv("ADMIN_EMAIL"), is_admin=True))
    db.commit()


event.listen(RegisteredUser.__table__, 'after_create', insert_initial_values)
