TABLA_CLIENTES = """
    CREATE TABLE IF NOT EXISTS Clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        direccion TEXT NOT NULL
    )
"""

TABLA_PRODUCTOS = """
    CREATE TABLE IF NOT EXISTS Productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INT NULL
    )
"""

TABLAS = [TABLA_CLIENTES, TABLA_PRODUCTOS]