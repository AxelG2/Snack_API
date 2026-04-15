from fastapi import FastAPI 
from pydantic import BaseModel 
import uvicorn

tags_metadata = [
    {"name": "Clientes", "description": "Operaciones de clientes"},
    {"name": "Productos", "description": "Operaciones de productos"},
    {"name": "Pedidos", "description": "Operaciones de pedidos"},
]

app = FastAPI(
    title="Snack API",
    description="API para gestionar snacks",
    version="1.0",
    openapi_tags=tags_metadata,
) 

class Cliente(BaseModel): 
    id: int
    nombre: str 
    telefono: str 
    direccion: str 

class ClienteCreate(BaseModel):
    nombre: str
    telefono: str
    direccion: str


class Producto(BaseModel): 
    id: int
    nombre: str 
    precio: float 
    stock: int 

class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int

class ProductoEnPedido(BaseModel):
    id: int
    cantidad: int


class Pedido(BaseModel): 
    id: int
    cliente_id: int 
    productos: list[ProductoEnPedido] # Lista de id de Productos + cantidad por producto
    total: float 

class PedidoCreate(BaseModel):
    cliente_id: int
    productos: list[ProductoEnPedido]


next_cliente_id = 1
next_producto_id = 1
next_pedido_id = 1


clientes = {} 
productos = {} 
pedidos = {} 


# Clientes
@app.get("/clientes", tags=["Clientes"])
def get_clientes(): 
    return clientes 

@app.get("/clientes/{cliente_id}", tags=["Clientes"]) 
def get_cliente(cliente_id: int): 
    if cliente_id in clientes: 
        return clientes[cliente_id] 
    return {"error": "Cliente no encontrado"} 

@app.post("/clientes", tags=["Clientes"]) 
def create_cliente(cliente: ClienteCreate):
    global next_cliente_id
    nuevo_cliente = Cliente(id=next_cliente_id, **cliente.model_dump())
    clientes[next_cliente_id] = nuevo_cliente
    next_cliente_id += 1
    return {"mensaje": "Cliente creado", "cliente": nuevo_cliente}

@app.delete("/clientes/{cliente_id}", tags=["Clientes"])
def delete_cliente(cliente_id: int):
    if cliente_id in clientes:
        del clientes[cliente_id]
        return {"mensaje": "Cliente eliminado"}
    return {"mensaje": "Cliente no encontrado"}


# Productos
@app.get("/productos", tags=["Productos"])
def get_productos(): 
    return productos 

@app.get("/productos/{producto_id}", tags=["Productos"]) 
def get_producto(producto_id: int): 
    if producto_id in productos: 
        return productos[producto_id] 
    return {"error": "Producto no encontrado"} 

@app.post("/productos", tags=["Productos"])
def post_producto(producto: ProductoCreate):
    global next_producto_id
    nuevo_producto = Producto(id=next_producto_id, **producto.model_dump())
    productos[next_producto_id] = nuevo_producto
    next_producto_id += 1
    return {"mensaje": "Producto agregado", "producto": nuevo_producto}

@app.delete("/productos/{producto_id}", tags=["Productos"])
def delete_producto(producto_id: int):
    if producto_id in productos:
        del productos[producto_id]
        return {"mensaje": "Producto eliminado"}
    return {"mensaje": "Producto no encontrado"}


# Pedidos
@app.post("/pedidos", tags=["Pedidos"]) 
def create_pedido(pedido: PedidoCreate):
    global next_pedido_id

    if pedido.cliente_id not in clientes:
        return {"error": "Cliente no encontrado"}

    total = 0.0
    for item in pedido.productos:
        if item.id not in productos:
            return {"error": f"Producto no encontrado: {item.id}"}
        if item.cantidad <= 0:
            return {"error": f"Cantidad invalida para producto {item.id}"}
        total += productos[item.id].precio * item.cantidad

    nuevo_pedido = Pedido(
        id=next_pedido_id,
        cliente_id=pedido.cliente_id,
        productos=pedido.productos,
        total=round(total, 2),
    )
    pedidos[next_pedido_id] = nuevo_pedido
    next_pedido_id += 1
    return {"mensaje": "Pedido creado", "pedido": nuevo_pedido}

@app.delete("/pedidos/{pedido_id}", tags=["Pedidos"]) 
def delete_pedido(pedido_id: int): 
    if pedido_id in pedidos: 
        del pedidos[pedido_id] 
        return {"mensaje": "Pedido eliminado"} 
    return {"error": "Pedido no encontrado"} 

@app.get("/pedidos", tags=["Pedidos"]) 
def get_pedidos(): 
    return pedidos 

@app.get("/pedidos/{pedido_id}", tags=["Pedidos"]) 
def get_pedido(pedido_id: int): 
    if pedido_id in pedidos: 
        return pedidos[pedido_id] 
    return {"error": "Pedido no encontrado"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)