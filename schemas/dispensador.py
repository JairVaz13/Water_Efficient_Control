from pydantic import BaseModel

# Esquema para crear un dispensador
class DispensadorCreate(BaseModel):
    estado: str
    id_recipiente: int
    token: str

# Esquema para actualizar un dispensador
class DispensadorUpdate(BaseModel):
    estado: str
    token: str

# Esquema para leer un dispensador
class Dispensador(BaseModel):
    id_dispensador: int
    estado: str
    id_recipiente: int
    token: str
