from pydantic import BaseModel, field_validator
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0

    @field_validator("precio")
    @classmethod
    def precio_positivo(cls, v):
        if v < 0: raise ValueError("El precio no puede ser negativo.")
        return v
    
    @field_validator("stock")
    @classmethod
    def stock_no_negativo(cls, v):
        if v < 0: raise ValueError("El stock no puede ser negativo.")
        return v

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None

class Producto(ProductoBase):
    id: int
    creado_en: str