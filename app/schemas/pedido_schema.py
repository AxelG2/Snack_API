from pydantic import BaseModel, Field
from typing import List

class ProductoEnPedido(BaseModel):
    id: int
    cantidad: int = Field(..., gt=0)

class PedidoCreate(BaseModel):
    cliente_id: int
    productos: List[ProductoEnPedido]

class PedidoResponse(PedidoCreate):
    id: int