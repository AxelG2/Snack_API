from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import clientes, productos, pedidos
from .database import inicializar
import uvicorn

app = FastAPI(
    title="Snack API",
    description="API para gestionar snacks"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En desarrollo está bien, en producción pon tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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