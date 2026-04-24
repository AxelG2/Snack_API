from fastapi import FastAPI
from .routes import clientes, productos, pedidos
from .database import inicializar
import uvicorn

app = FastAPI(
    title="Snack API",
    description="API para gestionar snacks"
)

app.include_router(clientes.router, prefix="/v1", tags=["Clientes"])
app.include_router(productos.router, prefix="/v1", tags=["Productos"])
app.include_router(pedidos.router, prefix="/v1/clientes/{cliente_id}", tags=["Pedidos"])

@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente."}

@app.on_event("startup")
def startup_event():
    inicializar()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)