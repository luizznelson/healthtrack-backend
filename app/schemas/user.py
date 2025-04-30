from pydantic import BaseModel, EmailStr
from typing import Optional
from typing import Optional
import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: Optional[str]
    created_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True
        from_attributes = True
        

class Token(BaseModel):
     access_token: str
     token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
