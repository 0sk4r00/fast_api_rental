from pydantic import BaseModel, EmailStr
from typing import Optional


class ItemBase(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(UserCreate):
    pass


class Item(ItemBase):
    id: int
    owner_id: int
    owner: UserOut
    in_stock: bool
    booked_by: str | None


class ItemCreate(ItemBase):
    pass


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
