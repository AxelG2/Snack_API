from ..schemas.cliente_schema import Cliente, ClienteCreate, ClienteUpdate
from ..database import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlite3 import Connection, IntegrityError
from typing import List

router = APIRouter()

@router.post("/", response_model=Cliente, status_code=201)
def crear_cliente(cliente: ClienteCreate, db: Connection = Depends(get_db)):
    try:
        cursor = db.execute("INSERT INTO Clientes (nombre, email, telefono, direccion) VALUES (?, ?, ?, ?)", (cliente.nombre, cliente.email, cliente.telefono, cliente.direccion),)
        db.commit()

        fila = db.execute("SELECT * FROM Clientes WHERE id=?", (cursor.lastrowid,)).fetchone()
        return dict(fila)
    except IntegrityError: raise HTTPException(409, "El email ya está registrado.")

@router.get("/", response_model=List[Cliente])
def listar_clientes(db: Connection = Depends(get_db)):
    clientes = db.execute("SELECT * FROM Clientes ORDER BY id").fetchall()
    return [dict(c) for c in clientes]

@router.get("/{id}", response_model=Cliente)
def obtener_cliente(id: int, db: Connection = Depends(get_db)):
    cliente = db.execute("SELECT * FROM Clientes WHERE id=?", (id,)).fetchone()
    if not cliente: raise HTTPException(404, "Cliente no encontrado.")
    return dict(cliente)

@router.patch("/{id}", response_model=Cliente)
def actualizar_cliente(id: int, datos: ClienteUpdate, db: Connection = Depends(get_db)):
    campos = {k: v for k, v in datos.model_dump().items() if v is not None}
    if not campos: raise HTTPException(400, "No se enviaron campos para actualizar.")

    set_clause = ", ".join(f"{k}=?" for k in campos)

    try:
        db.execute(f"UPDATE Clientes SET {set_clause} WHERE id=?", (*campos.values(), id))
        db.commit()
    except IntegrityError: raise HTTPException(409, "El email ya está en uso.")

    fila = db.execute("SELECT * FROM Clientes WHERE id=?", (id,)).fetchone()
    if not fila: raise HTTPException(404, "Cliente no encontrado.")

    return dict(fila)

@router.delete("/{id}", status_code=204)
def borrar_cliente(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("DELETE FROM Clientes WHERE id=?", (id,))
    db.commit()
    if cursor.rowcount == 0: raise HTTPException(404, "Cliente no encontrado.")