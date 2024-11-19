from pydantic import BaseModel
from typing import Optional

class ContainerBase(BaseModel):
    ubicacion: Optional[str] = None
    tipo: str
    capacidad: int

class ContainerCreate(ContainerBase):
    ubicacion: Optional[str] = None
    tipo: Optional[str] = None
    capacidad: Optional[int] = None
    token: str
    
class ContainerUpdate(BaseModel):
    ubicacion: Optional[str] = None
    tipo: Optional[str] = None
    capacidad: Optional[int] = None
