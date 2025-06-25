from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    user_id: int

    class Config:
        orm_mode = True

class ProductBulkCreate(BaseModel):
    products: List[ProductCreate]
