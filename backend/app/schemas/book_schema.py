from pydantic import BaseModel, Field, ConfigDict


class BookCreate(BaseModel):
    title: str
    author: str
    description: str | None = None
    category_id: int
    rating: int = Field(ge=1, le=5)


class BookUpdate(BaseModel):
    title: str
    author: str
    description: str | None = None
    category_id: int
    rating: int = Field(ge=1, le=5)


class BookResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    title: str
    author: str
    description: str | None
    category_id: int
    rating: int
