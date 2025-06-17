from pydantic import BaseModel, EmailStr
from datetime import datetime
class TodoItem(BaseModel):
    title: str
    description: str
    is_completed: bool = False
    is_deleted: bool = False
    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()   

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str