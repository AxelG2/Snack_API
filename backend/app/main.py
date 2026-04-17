from fastapi import FastAPI
from .routes import clientes, productos
from .database import inicializar
import uvicorn

app = FastAPI(
    title="Snack API",
    description="API para gestionar snacks"
)

app.include_router(clientes.router, prefix="/v1", tags=["Clientes"])
app.include_router(productos.router, prefix="/v1", tags=["Productos"])

@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente."}

@app.on_event("startup")
def startup_event():
    inicializar()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

# class ProductoEnPedido(BaseModel):
#     id: int
#     cantidad: int

# class Pedido(BaseModel): 
#     id: int
#     cliente_id: int 
#     productos: list[ProductoEnPedido] # Lista de id de Productos + cantidad por producto
#     total: float 

# class PedidoCreate(BaseModel):
#     cliente_id: int
#     productos: list[ProductoEnPedido]

# pedidos = {} 

# # Pedidos
# @app.post("/pedidos", tags=["Pedidos"]) 
# def create_pedido(pedido: PedidoCreate):
#     global next_pedido_id

#     if pedido.cliente_id not in clientes:
#         return {"error": "Cliente no encontrado"}

#     total = 0.0
#     for item in pedido.productos:
#         if item.id not in productos:
#             return {"error": f"Producto no encontrado: {item.id}"}
#         if item.cantidad <= 0:
#             return {"error": f"Cantidad invalida para producto {item.id}"}
#         total += productos[item.id].precio * item.cantidad

#     nuevo_pedido = Pedido(
#         id=next_pedido_id,
#         cliente_id=pedido.cliente_id,
#         productos=pedido.productos,
#         total=round(total, 2),
#     )
#     pedidos[next_pedido_id] = nuevo_pedido
#     next_pedido_id += 1
#     return {"mensaje": "Pedido creado", "pedido": nuevo_pedido}

# @app.delete("/pedidos/{pedido_id}", tags=["Pedidos"]) 
# def delete_pedido(pedido_id: int): 
#     if pedido_id in pedidos: 
#         del pedidos[pedido_id] 
#         return {"mensaje": "Pedido eliminado"} 
#     return {"error": "Pedido no encontrado"} 

# @app.get("/pedidos", tags=["Pedidos"]) 
# def get_pedidos(): 
#     return pedidos 

# @app.get("/pedidos/{pedido_id}", tags=["Pedidos"]) 
# def get_pedido(pedido_id: int): 
#     if pedido_id in pedidos: 
#         return pedidos[pedido_id] 
#     return {"error": "Pedido no encontrado"}