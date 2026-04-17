TABLA_CLIENTES = """
    CREATE TABLE IF NOT EXISTS Clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        direccion TEXT NOT NULL
    )
"""

TABLAS = [TABLA_CLIENTES]