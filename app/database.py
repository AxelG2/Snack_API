from .models.database_models import TABLAS
import sqlite3
from pathlib import Path

DB_PATH = Path("data/snacks.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def get_db():
    conn = get_connection()
    try: yield conn
    finally: conn.close()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Clientes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            telefono    TEXT,
            direccion   TEXT,
            creado_en   TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS Productos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT    NOT NULL,
            descripcion TEXT,
            precio      REAL    NOT NULL CHECK(precio >= 0),
            stock       INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
            creado_en   TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS Pedidos (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id   INTEGER NOT NULL REFERENCES Clientes(id),
            estado       TEXT    NOT NULL DEFAULT 'pendiente' CHECK(estado IN ('pendiente','enviado','entregado','cancelado')),
            total        REAL    NOT NULL DEFAULT 0,
            creado_en    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS PedidoItems (
            pedido_id   INTEGER NOT NULL REFERENCES Pedidos(id) ON DELETE CASCADE,
            producto_id INTEGER NOT NULL REFERENCES Productos(id),
            cantidad    INTEGER NOT NULL CHECK(cantidad > 0),
            precio_unit REAL    NOT NULL
        );
    """)

    conn.commit()
    conn.close()
    print("Base de datos inicializada.")