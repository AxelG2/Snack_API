from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteBase(BaseModel): 
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class Cliente(ClienteBase):
    id: int
    creado_en: str