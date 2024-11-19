from pydantic import BaseModel

class UserBase(BaseModel):
    nombre: str
    email: str

class UserCreate(UserBase):
    contrasena: str

