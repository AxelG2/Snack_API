from ..schemas.pedido_schema import Pedido, PedidoCreate, PedidoEstadoUpdate, PedidoGetAll
from ..database import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlite3 import Connection
from typing import List

router = APIRouter()

def devolver_stock(pedido_id: int, db: Connection):
    detalle_pedido = [dict(d) for d in db.execute("SELECT cantidad, producto_id FROM PedidoItems WHERE pedido_id=?", (pedido_id,)).fetchall()]

    for detalle in detalle_pedido:
        _cantidad = dict(db.execute("SELECT stock FROM Productos WHERE id=?", (detalle["producto_id"],)).fetchone())

        db.execute("UPDATE Productos SET stock=stock+? WHERE id=?", (detalle['cantidad'], detalle['producto_id'],))

        _cantidad_actualizada = dict(db.execute("SELECT stock FROM Productos WHERE id=?", (detalle['producto_id'],)).fetchone())

        if _cantidad['stock'] == _cantidad_actualizada['stock']:
            db.rollback()
            raise HTTPException(500, f"Actualización de stock no relizada. Producto: {detalle['producto_id']}.")

@router.post("/", response_model=Pedido, status_code=201)
def crear_pedido(pedido: PedidoCreate, db: Connection = Depends(get_db)):
    if not db.execute("SELECT 1 FROM Clientes WHERE id=? LIMIT 1", (pedido.cliente_id,)).fetchone(): raise HTTPException(404, "Cliente no encontrado.")

    if not pedido.items: raise HTTPException(400, "El pedido debe tener al menos un item.")

    total = 0.0
    items_data = []

    for item in pedido.items:
        producto = db.execute("SELECT nombre, precio, stock FROM Productos WHERE id=?", (item.producto_id,)).fetchone()
        if not producto: raise HTTPException(404, "Producto no encontrado.")
        if producto['stock'] < item.cantidad: raise HTTPException(409, f"Stock insuficiente para '{producto['nombre']}' (disponible: {producto['stock']}).")

        subtotal = producto["precio"] * item.cantidad
        total += subtotal

        items_data.append({
            "producto_id": item.producto_id,
            "cantidad": item.cantidad,
            "precio_unit": producto['precio']
        })

    cursor = db.execute("INSERT INTO Pedidos (cliente_id, total) VALUES (?, ?)", (pedido.cliente_id, total,))
    id = cursor.lastrowid

    for item in items_data:
        db.execute("INSERT INTO PedidoItems (pedido_id, producto_id, cantidad, precio_unit) VALUES (?, ?, ?, ?)", (id, item['producto_id'], item['cantidad'], item['precio_unit'],))

        db.execute("UPDATE Productos SET stock=stock-? WHERE id=?", (item['cantidad'], item['producto_id'],))
    db.commit()

    pedido_creado = dict(db.execute("SELECT * FROM Pedidos WHERE id=?", (id,)).fetchone())
    pedido_creado = {
        **pedido_creado, 
        "items": [dict(i) for i in db.execute("SELECT producto_id, cantidad, (precio_unit*cantidad) AS subtotal FROM PedidoItems WHERE pedido_id=?", (id,)).fetchall()]
    }

    return pedido_creado

@router.get("/", response_model=List[PedidoGetAll])
def listar_todos_los_pedidos(db: Connection = Depends(get_db)):
    pedidos = db.execute("SELECT * FROM Pedidos ORDER BY id").fetchall()
    if not pedidos: raise HTTPException(404, "Pedidos no encontrados.")

    return [dict(p) for p in pedidos]

@router.get("/cliente/{cliente_id}", response_model=List[PedidoGetAll])
def listar_pedidos_por_cliente(cliente_id: int, db: Connection = Depends(get_db)):
    pedidos = db.execute("SELECT * FROM Pedidos WHERE cliente_id=? ORDER BY id", (cliente_id,)).fetchall()
    if not pedidos: raise HTTPException(404, "Pedidos no encontrados.")

    return [dict(p) for p in pedidos]

@router.get("/{pedido_id}", response_model=Pedido)
def obtener_pedido(pedido_id: int, db: Connection = Depends(get_db)):
    pedido = db.execute("SELECT * FROM Pedidos WHERE id=?", (pedido_id,)).fetchone()
    if not pedido: raise HTTPException(404, "Pedido no encontrado.")

    pedido_items = db.execute("SELECT producto_id, cantidad, (cantidad*precio_unit) AS subtotal FROM PedidoItems WHERE pedido_id=?", (pedido_id,)).fetchall()
    if not pedido_items: pedido_items = []

    pedido = {**dict(pedido), "items": [dict(i) for i in pedido_items]}
    return pedido

@router.patch("/{pedido_id}", response_model=PedidoGetAll)
def actualizar_estado(pedido_id: int, pedido: PedidoEstadoUpdate, db: Connection = Depends(get_db)):
    estado_actual = db.execute("SELECT estado FROM Pedidos WHERE id=?", (pedido_id,)).fetchone()
    if not estado_actual: raise HTTPException(404, "Pedido no encontrado.")

    if pedido.estado not in ["pendiente", "enviado", "entregado", "cancelado"]: raise HTTPException(400, "Estado no válido.")
    
    estado_actual = dict(estado_actual)
    if estado_actual['estado'] == "cancelado": raise HTTPException(409, f"El pedido está cancelado, ya no se puede cambiar el estado. Pedido: {pedido_id}.")

    if pedido.estado in estado_actual: raise HTTPException(409, "Estado ya seleccionado.")

    db.execute("UPDATE Pedidos SET estado=? WHERE id=?", (pedido.estado, pedido_id,))
    if pedido.estado == "cancelado": devolver_stock(pedido_id, db)
    db.commit()

    res = dict(db.execute("SELECT * FROM Pedidos WHERE id=?", (pedido_id,)).fetchone())
    return res

@router.delete("/{pedido_id}", status_code=204)
def eliminar_pedido(pedido_id: int, db: Connection = Depends(get_db)):
    estado = dict(db.execute("SELECT estado FROM Pedidos WHERE id=?", (pedido_id,)).fetchone())
    if not estado: raise HTTPException(404, "Pedido no encontrado.")

    estado = dict(estado)
    if estado['estado'] != "cancelado": devolver_stock(pedido_id, db)

    db.execute("DELETE FROM Pedidos WHERE id=?", (pedido_id,))
    db.commit()