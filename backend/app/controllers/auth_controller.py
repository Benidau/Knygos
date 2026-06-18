from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import *
from app.auth.hashing import *
from app.auth.jwt_handler import *

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    request: UserRegister,
    db: Session = Depends(get_db)
):

    user = User(
        name=request.name,
        surname=request.surname,
        email=request.email,
        password_hash=hash_password(request.password),
        role=request.role,  

    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful"
    }


@router.post("/login")
def login(
    request: UserLogin, 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == request.email 
    ).first()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "user_id": user.id,
            "role": user.role
        }
    )

    # Grąžina tvarkingą JSON atsakymą
    return {
        "access_token": token,
        "token_type": "bearer"
    }