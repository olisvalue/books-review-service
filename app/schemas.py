from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str

    class ConfigDict:
        from_attributes = True

class BookCreate(BaseModel):
    title: str
    author: str

class BookResponse(BaseModel):
    id: int
    title: str
    author: str

    class ConfigDict:
        from_attributes = True

class ReviewCreate(BaseModel):
    rating: int
    comment: str
    book_id: int

class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str
    book_id: int
    username: str

    class ConfigDict:
        from_attributes = True

class TokenData(BaseModel):
    username: str  

class Token(BaseModel):
    access_token: str
    token_type: str
