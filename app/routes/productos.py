from ..schemas.producto_schema import ProductoCreate, ProductoResponse, ProductoUpdate
from ..database import conectar
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

@router.post("/productos", response_model=ProductoResponse, status_code=201)
def crear_producto(producto: ProductoCreate):
    with conectar() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Productos (nombre, precio, stock) VALUES (?, ?, ?)", (producto.nombre, producto.precio, producto.stock,))

            id = cursor.lastrowid

            return {**producto.model_dump(), 'id': id}
        except:
            raise HTTPException(400, "Error al crear el producto.")

@router.get("/productos", response_model=List[ProductoResponse])
def listar_productos():
    with conectar() as conn:
        productos = conn.execute("SELECT * FROM Productos").fetchall()
        return [dict(p) for p in productos]
    
@router.get("/productos/{id}", response_model=ProductoResponse)
def obtener_producto(id: int):
    with conectar() as conn:
        producto = conn.execute("SELECT * FROM Productos WHERE id = ?", (id,)).fetchone()

        if producto is None: raise HTTPException(404, "Producto no encontrado.")

        return dict(producto)
    
@router.patch("/productos/{id}", response_model=ProductoResponse)
def actualizar_producto(id: int, producto_data: ProductoUpdate):
    with conectar() as conn:
        producto = conn.execute("SELECT * FROM Productos WHERE id = ?", (id,)).fetchone()

        if producto is None: raise HTTPException(404, "Producto no encontrado.")

        update_producto = producto_data.model_dump(exclude_unset=True)
        if not update_producto: raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar.")

        campos = ", ".join([f"{k} = ?" for k in update_producto.keys()])
        valores = list(update_producto.values())
        valores.append(id)

        cursor = conn.cursor()

        cursor.execute(f"UPDATE Productos SET {campos} WHERE id = ?", valores,)

        respuesta = conn.execute("SELECT * FROM Productos WHERE id = ?", (id,)).fetchone()
        return dict(respuesta)
    
@router.delete("/productos/{id}", status_code=204)
def borrar_producto(id: int):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Productos WHERE id = ?", (id,))

        if cursor.rowcount == 0: raise HTTPException(404, "Producto no encontrado.")

        return None