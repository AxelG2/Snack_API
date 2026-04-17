from ..schemas.cliente_schema import ClienteBase, ClienteResponse
from ..database import conectar
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

@router.post("/clientes", response_model=ClienteResponse, status_code=201)
def crear_cliente(cliente: ClienteBase):
    with conectar() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Clientes (nombre, telefono, direccion) VALUES (?, ?, ?)", (cliente.nombre, cliente.telefono, cliente.direccion,))

            id = cursor.lastrowid

            return {**cliente.model_dump(), 'id': id}
        except:
            raise HTTPException(400, "Error al crear al cliente.")
        

@router.get("/clientes", response_model=List[ClienteResponse])
def listar_clientes():
    with conectar() as conn:
        clientes = conn.execute("SELECT * FROM Clientes").fetchall()
        return [dict(c) for c in clientes]
    
@router.get("/clientes/{id}", response_model=ClienteResponse)
def obtener_cliente(id: int):
    with conectar() as conn:
        cliente = conn.execute("SELECT * FROM Clientes WHERE id = ?", (id,)).fetchone()

        if cliente is None: raise HTTPException(404, "Cliente no encontrado.")

        return dict(cliente)
    
# TODO: UPDATE

@router.delete("/clientes/{id}", status_code=204)
def borrar_cliente(id: int):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clientes WHERE id = ?", (id,))

        if cursor.rowcount == 0: raise HTTPException(404, "Cliente no encontrado.")

        return None