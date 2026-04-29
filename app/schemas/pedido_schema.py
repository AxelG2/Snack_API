from pydantic import BaseModel, field_validator
from typing import List

class PedidoItemCreate(BaseModel):
    producto_id: int
    cantidad: int

    @field_validator("cantidad")
    @classmethod
    def cantidad_positiva(cls, v):
        if v <= 0: raise ValueError("La cantidad debe ser mayor a 0.")
        return v
    
class PedidoItem(BaseModel):
    producto_id: int
    cantidad: int
    subtotal: float

class PedidoCreate(BaseModel):
    cliente_id: int
    items: List[PedidoItemCreate]

class PedidoEstadoUpdate(BaseModel):
    estado: str

class Pedido(BaseModel):
    id: int
    cliente_id: int
    estado: str
    total: float
    creado_en: str
    items: List[PedidoItem]

class PedidoGetAll(BaseModel):
    id: int
    cliente_id: int
    estado: str
    total: float
    creado_en: str