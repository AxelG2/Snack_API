from .models.database_models import TABLAS
import sqlite3
import os

DB_PATH = "data/snacks.db"

def conectar():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def inicializar():
    with conectar() as conn:
        for tabla in TABLAS:
            conn.execute(tabla)
        conn.commit()