import pytest
from datetime import timedelta
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    settings
)


def test_verify_password_correct():
    plain = "testpassword123"
    hashed = get_password_hash(plain)
    assert verify_password(plain, hashed) is True


def test_verify_password_incorrect():
    plain = "testpassword123"
    hashed = get_password_hash(plain)
    assert verify_password("wrongpassword", hashed) is False


def test_get_password_hash_unique():
    hash1 = get_password_hash("password")
    hash2 = get_password_hash("password")
    assert hash1 != hash2  # bcrypt should generate different salts


def test_create_access_token():
    data = {"sub": "123", "email": "test@example.com"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_access_token_expiration():
    data = {"sub": "123"}
    token = create_access_token(data, expires_delta=timedelta(minutes=5))
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "123"
    assert payload["type"] == "access"


def test_create_refresh_token():
    data = {"sub": "123"}
    token = create_refresh_token(data)
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "123"
    assert payload["type"] == "refresh"


def test_decode_token_valid():
    data = {"sub": "123", "custom": "value"}
    token = create_access_token(data)
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "123"
    assert payload["custom"] == "value"


def test_decode_token_invalid():
    invalid_token = "invalid.token.here"
    payload = decode_token(invalid_token)
    assert payload is None


def test_decode_token_expired():
    import time
    data = {"sub": "123"}
    # Create a token that expired already
    from datetime import datetime, timezone
    from jose import jwt
    expire = datetime.now(timezone.utc) - timedelta(minutes=10)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "access"})
    expired_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    payload = decode_token(expired_token)
    assert payload is None
