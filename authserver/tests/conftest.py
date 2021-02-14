import tempfile
import os

import pytest
from app.db import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model.registered_user import RegisteredUser


@pytest.fixture(scope="session", autouse=True)
def test_app():
    client = TestClient(app)

    _, db_fname = tempfile.mkstemp()
    TESTING_DB_URL = "sqlite:///" + db_fname

    engine = create_engine(TESTING_DB_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def get_testing_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    db = next(get_testing_db())
    db.add(RegisteredUser(email=os.getenv("ADMIN_EMAIL"), is_admin=True))
    db.commit()

    app.dependency_overrides[get_db] = get_testing_db

    yield client  # testing happens here
