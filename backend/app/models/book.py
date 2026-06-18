from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String(255))
    author = Column(String(255))
    description = Column(String(500))
    category_id = Column(Integer, ForeignKey("categories.id"))
    rating = Column(Integer)