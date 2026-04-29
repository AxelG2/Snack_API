from ..schemas.producto_schema import Producto, ProductoCreate, ProductoUpdate
from ..database import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlite3 import Connection
from typing import List

router = APIRouter()

@router.post("/", response_model=Producto, status_code=201)
def crear_producto(producto: ProductoCreate, db: Connection = Depends(get_db)):
    cursor = db.execute("INSERT INTO Productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)", (producto.nombre, producto.descripcion, producto.precio, producto.stock,))
    db.commit()

    fila = db.execute("SELECT * FROM Productos WHERE id=?", (cursor.lastrowid,)).fetchone()
    return dict(fila)

@router.get("/", response_model=List[Producto])
def listar_productos(db: Connection = Depends(get_db)):
    productos = db.execute("SELECT * FROM Productos ORDER BY id").fetchall()
    return [dict(p) for p in productos]

@router.get("/{id}", response_model=Producto)
def obtener_producto(id: int, db: Connection = Depends(get_db)):
    producto = db.execute("SELECT * FROM Productos WHERE id=?", (id,)).fetchone()
    if not producto: raise HTTPException(404, "Producto no encontrado.")
    return dict(producto)

@router.patch("/{id}", response_model=Producto)
def actualizar_producto(id: int, datos: ProductoUpdate, db: Connection = Depends(get_db)):
    campos = {k: v for k, v in datos.model_dump().items() if v is not None}
    if not campos: raise HTTPException(400, "No se enviaron campos para actualizar.")

    set_clause = ", ".join(f"{k}=?" for k in campos)

    db.execute(f"UPDATE Productos SET {set_clause} WHERE id=?", (*campos.values(), id))
    db.commit()

    fila = db.execute("SELECT * FROM Productos WHERE id=?", (id,)).fetchone()
    if not fila: raise HTTPException(404, "Producto no encontrado.")

    return dict(fila)

@router.delete("/{id}", status_code=204)
def borrar_producto(id: int, db: Connection = Depends(get_db)):
    cursor = db.execute("DELETE FROM Productos WHERE id=?", (id,))
    db.commit()
    if cursor.rowcount == 0: raise HTTPException(404, "Producto no encontrado.")