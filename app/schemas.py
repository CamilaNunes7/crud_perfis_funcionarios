from pydantic import BaseModel, EmailStr
from typing import Optional

# Modelo Base do usuário
class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    role: str
    department: str

# Modelo para criação do usuário
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    department: str
    password: str

# Modelo para update do usuário
class UserUpdate(UserBase):
    password: Optional[str] = None

# Modelo de saída
class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

