from jose import jwt
from jose import JWTError

from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.config import *

from fastapi.security import HTTPBearer 

security = HTTPBearer()

def get_current_user(
    credentials = Depends(security), 
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,         
            algorithms=[JWT_ALGORITHM] 
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
            
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def admin_required(user=Depends(get_current_user)):
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Administrator access required"
        )
    return user