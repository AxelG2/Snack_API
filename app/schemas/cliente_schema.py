from pydantic import BaseModel, Field

class ClienteBase(BaseModel): 
    nombre: str
    telefono: str = Field(..., max_length=10)
    direccion: str = Field(..., max_length=50)

# class ClienteCreate(ClienteBase):
#     pass

class ClienteResponse(ClienteBase):
    id: int