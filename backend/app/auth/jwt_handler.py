from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM

def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )