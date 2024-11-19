from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    nombre: str
    email: EmailStr

class UserCreate(UserBase):
    contrasena: str

