from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .routes import clientes, productos, pedidos
from . import database
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield

app = FastAPI(
    title="Snack API",
    description="API para gestionar snacks",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En desarrollo está bien, en producción pon tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router, prefix="/v2/clientes", tags=["Clientes"])
app.include_router(productos.router, prefix="/v2/productos", tags=["Productos"])
app.include_router(pedidos.router, prefix="/v2/pedidos", tags=["Pedidos"])

@app.get("/")
def home(): return {"mensaje": "API funcionando correctamente."}

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)