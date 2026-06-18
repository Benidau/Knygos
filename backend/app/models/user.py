from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, text
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(55), nullable=False)
    surname = Column(String(55), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        Enum("USER", "ADMIN"),
        nullable=False,
        server_default="USER"
    )
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )