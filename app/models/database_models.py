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

TABLA_PEDIDOS = """
    CREATE TABLE IF NOT EXISTS Pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        fecha TEXT NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES Clientes(id) ON DELETE CASCADE
    )
"""

TABLA_DETALLE_PEDIDO = """
    CREATE TABLE IF NOT EXISTS DetallePedido (
        pedido_id INTEGER,
        producto_id INTEGER,
        cantidad INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES Pedidos(id) ON DELETE CASCADE,
        FOREIGN KEY (producto_id) REFERENCES Productos(id) ON DELETE CASCADE
    )
"""

TABLAS = [TABLA_CLIENTES, TABLA_PRODUCTOS, TABLA_PEDIDOS, TABLA_DETALLE_PEDIDO]