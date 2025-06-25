from pydantic import BaseModel

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
    description: str = None

class ProductOut(BaseModel):
    id: int
    name: str
    description: str = None
    user_id: int

    class Config:
        orm_mode = True
