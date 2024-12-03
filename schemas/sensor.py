from pydantic import BaseModel
from typing import Optional


class SensorBase(BaseModel):
    tipo: str
    token: str

class SensorCreate(SensorBase):
    tipo: Optional[str] = None
    token: str
    id_recipienre: int
    
class SensorUpdate(BaseModel):
    tipo: Optional[str] = None


class IARecipienteSensorCreate(BaseModel):
    id_recipiente: int
    id_sensor: int
    valor: float
    fecha: str 

class SensorData(BaseModel):
    id_recipiente: int
    id_sensor: int
    valor: float
    tipo_sensor: str
    fecha: str