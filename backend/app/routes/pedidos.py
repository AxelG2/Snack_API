from ..schemas.pedido_schema import PedidoCreate
from ..database import conectar
from fastapi import APIRouter, HTTPException
from datetime import datetime
import sqlite3

router = APIRouter()

@router.post("/pedidos", status_code=201)
def crear_pedido(pedido: PedidoCreate):
    with conectar() as conn:
        try:
            cliente_id = pedido.cliente_id
            if not conn.execute("SELECT EXISTS(SELECT 1 FROM Clientes WHERE id = ?)", (cliente_id,)): raise HTTPException(404, "No existe el cliente.")

            total = 0
            lista_productos = []

            for producto in pedido.productos:
                existe_producto = conn.execute("SELECT * FROM Productos WHERE id = ?", (producto.id,)).fetchone()
                if not existe_producto: raise HTTPException(404, f"No existe el producto {producto.id}.")

                stock = existe_producto[3]
                if stock == 0: print(f"No hay existencia del producto {producto.id}")

                precio = existe_producto[2]
                subtotal = precio * producto.cantidad
                total += subtotal

                lista_productos.append({**producto.model_dump(), 'subtotal': subtotal})

            cursor = conn.cursor()
            cursor.execute("INSERT INTO Pedidos (cliente_id, fecha, total) VALUES (?, ?, ?)", (cliente_id, datetime.now(), total,))

            id = cursor.lastrowid

            for producto in lista_productos:
                cursor.execute("INSERT INTO DetallePedido (pedido_id, producto_id, cantidad, subtotal) VALUES (?, ?, ?, ?)", (id, producto['id'], producto['cantidad'], producto['subtotal'],))

            return {'msg': 'Pedido creado exitosamente.', 'id': id}
        except Exception as e: raise HTTPException(500, f"Error al guardar: {str(e)}")

@router.get("/pedidos", status_code=200)
def obtener_pedidos_por_cliente(cliente_id: int):
    with conectar() as conn:
        try:
            if not conn.execute("SELECT EXISTS(SELECT 1 FROM Clientes WHERE id = ?)", (cliente_id,)): raise HTTPException(404, "No existe el cliente.")

            query = """
                SELECT dp.* FROM DetallePedido dp
                JOIN Pedidos p ON dp.pedido_id = p.id
                WHERE p.cliente_id = ?
            """
            pedidos = conn.execute(query, (cliente_id,)).fetchall()
            if not pedidos: raise HTTPException(404, "No existen pedidos con este cliente.")

            return pedidos
        except sqlite3.Error as e: raise HTTPException(500, f"Error de base de datos: {str(e)}")
        except HTTPException: raise
        except Exception as e: raise HTTPException(500, "Error interno inesperado.")

@router.get("/pedidos/{pedido_id}", status_code=200)
def obtener_pedido(cliente_id: int, pedido_id: int):
    with conectar() as conn:
        try:
            query = """
                SELECT dp.* FROM DetallePedido dp
                JOIN Pedidos p ON dp.pedido_id = p.id
                WHERE p.cliente_id = ? AND p.id = ?
            """
            pedido = conn.execute(query, (cliente_id, pedido_id,)).fetchone()
            if not pedido: raise HTTPException(404, "Pedido no encontrado.")

            return pedido
        except sqlite3.Error as e: raise HTTPException(500, f"Error de base de datos: {str(e)}")
        except HTTPException: raise
        except Exception as e: raise HTTPException(500, "Error interno inesperado.")