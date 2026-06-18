from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User
from app.models.book import Book
from app.models.category import Category
from typing import List
from app.schemas.book_schema import (BookCreate, BookUpdate, BookResponse)
from app.schemas.category_schema import CategoryCreate, CategoryResponse

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# READ
@router.get("/", response_model=list[BookResponse])
def get_all_books(
    category: str | None = None,
    sort: str | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if user_id is not None and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can filter books by user_id"
        )

    query = db.query(Book)

    if category:
        category_obj = db.query(Category).filter(Category.name == category).first()
        
        if not category_obj:
            raise HTTPException(
                status_code=404,  
                detail="Category does not exist"
            )
        
        query = query.filter(Book.category_id == category_obj.id)

    if user_id:
        query = query.filter(Book.user_id == user_id)

    if sort == "asc":
        query = query.order_by(Book.rating.asc())
    elif sort == "desc":
        query = query.order_by(Book.rating.desc())

    return query.all()


@router.get("/my", response_model=list[BookResponse])
def get_my_books(
    category: str | None = None,  
    sort: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(Book).filter(Book.user_id == current_user.id)

    if category:
        category_obj = db.query(Category).filter(Category.name == category).first()
        if not category_obj:
            raise HTTPException(
                status_code=404,  
                detail="Category does not exist"
            )
        query = query.filter(Book.category_id == category_obj.id)  

    if sort == "asc":
        query = query.order_by(Book.rating.asc())
    elif sort == "desc":
        query = query.order_by(Book.rating.desc())

    return query.all()


# CREATE
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(
    request: BookCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    category_exists = db.query(Category).filter(Category.id == request.category_id).first()
    if not category_exists:
        raise HTTPException(
            status_code=400,
            detail="Invalid category_id. Please provide an existing category ID."
        )

    book = Book(
        title=request.title,
        author=request.author,
        description=request.description,
        category_id=request.category_id,  
        rating=request.rating,
        user_id=user.id
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    request: CategoryCreate,  
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403, 
            detail="Only administrators can perform this action"
        )

    existing_category = db.query(Category).filter(Category.name == request.name).first()
    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )
    
    new_category = Category(name=request.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


# UPDATE
@router.put("/{id}", response_model=BookResponse)
def update_book(
    id: int,
    request: BookUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if book.user_id != user.id and user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this book"
        )

    category_exists = db.query(Category).filter(Category.id == request.category_id).first()
    if not category_exists:
        raise HTTPException(
            status_code=400,
            detail="Invalid category_id. Please provide an existing category ID."
        )

    book.title = request.title
    book.author = request.author
    book.description = request.description
    book.category_id = request.category_id  
    book.rating = request.rating

    db.commit()
    db.refresh(book)

    return book


# DELETE
@router.delete("/{id}")
def delete_book(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if book.user_id != user.id and user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this book"
        )

    db.delete(book)
    db.commit()

    return {
        "message": "Book deleted successfully"
    }