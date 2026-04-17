from pydantic import BaseModel, Field
from typing import Optional

class ProductoBase(BaseModel):
    precio: float
    stock: int

class ProductoCreate(ProductoBase):
    nombre: str

class ProductoUpdate(ProductoBase):
    precio: Optional[float] = None
    stock: Optional[int] = None

class ProductoResponse(ProductoBase):
    id: int
    nombre: str