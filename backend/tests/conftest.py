import os
import sys
import time
from typing import Generator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# Add backend directory to path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import app modules
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from fastapi.testclient import TestClient
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate

# Use test database
settings.DATABASE_URL = settings.DATABASE_URL_TEST

# Create test engine
test_engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)


@pytest.fixture(scope="session")
def db_engine():
    """Create all tables for test session."""
    # Drop all tables first to ensure clean state, then create
    try:
        Base.metadata.drop_all(bind=test_engine)
    except Exception:
        pass
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    # Cleanup: close all connections first, then drop tables
    test_engine.dispose()
    try:
        Base.metadata.drop_all(bind=test_engine)
    except Exception:
        pass


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a new database session for each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def app_override(db_session):
    """Override get_db dependency to use test session."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield app
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(app_override):
    """Test client for API endpoints."""
    with TestClient(app_override) as c:
        yield c


@pytest.fixture(scope="function")
def normal_user(db_session):
    """Create a normal user with unique email."""
    auth_service = AuthService(db_session)
    unique = int(time.time() * 1000) % 1000000
    user_in = UserCreate(
        email=f"testuser{unique}@example.com",
        username=f"testuser{unique}",
        password="testpassword123"
    )
    user, _ = auth_service.register(user_in)
    return user


@pytest.fixture(scope="function")
def admin_user(db_session):
    """Create an admin user with unique email."""
    from app.models.user import User as UserModel
    auth_service = AuthService(db_session)
    unique = int(time.time() * 1000) % 1000000
    user_in = UserCreate(
        email=f"admin{unique}@example.com",
        username=f"adminuser{unique}",
        password="adminpassword123"
    )
    user, _ = auth_service.register(user_in)
    # Promote to admin
    user_obj = db_session.query(UserModel).filter(UserModel.id == user.id).first()
    user_obj.is_admin = True
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def user_token(normal_user):
    """Return access token for normal user."""
    from app.core.security import create_access_token
    token_data = {"sub": str(normal_user.id)}
    return create_access_token(token_data)


@pytest.fixture(scope="function")
def admin_token(admin_user):
    """Return access token for admin user."""
    from app.core.security import create_access_token
    token_data = {"sub": str(admin_user.id)}
    return create_access_token(token_data)
