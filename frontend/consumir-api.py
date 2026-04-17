import requests


BASE_URL = "http://127.0.0.1:8000"


def _print_response(response):
    print(f"Status: {response.status_code}")
    try:
        print("Body:", response.json())
    except ValueError:
        print("Body:", response.text)
    print("-" * 60)


def _print_listado(titulo, response):
    print(f"Status: {response.status_code}")

    if response.status_code >= 400:
        _print_response(response)
        return

    try:
        data = response.json()
    except ValueError:
        print("No se pudo leer la respuesta como JSON.")
        print("Body:", response.text)
        print("-" * 60)
        return

    if not isinstance(data, dict) or not data:
        print(f"\n{titulo}")
        print("- (sin registros)")
        print("-" * 60)
        return

    print(f"\n{titulo}")
    for item_id in sorted(data.keys(), key=lambda x: int(x)):
        item = data[item_id]

        if "cliente_id" in item:
            productos_txt = ", ".join(
                [f"id={p['id']} x{p['cantidad']}" for p in item.get("productos", [])]
            )
            print(
                f"- ID {item.get('id')}: cliente={item.get('cliente_id')} | "
                f"productos=[{productos_txt}] | total={item.get('total')}"
            )
        elif "stock" in item:
            print(
                f"- ID {item.get('id')}: {item.get('nombre')} | "
                f"precio={item.get('precio')} | stock={item.get('stock')}"
            )
        else:
            print(
                f"- ID {item.get('id')}: {item.get('nombre')} | "
                f"tel={item.get('telefono')} | dir={item.get('direccion')}"
            )

    print("-" * 60)


def _safe_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Ingresa un numero valido.")


def _safe_float(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Ingresa un numero decimal valido.")


# Clientes

def crear_cliente():
    payload = {
        "nombre": input("Nombre: ").strip(),
        "telefono": input("Telefono: ").strip(),
        "direccion": input("Direccion: ").strip(),
    }
    response = requests.post(f"{BASE_URL}/clientes", json=payload, timeout=10)
    _print_response(response)


def listar_clientes():
    response = requests.get(f"{BASE_URL}/clientes", timeout=10)
    _print_listado("Lista de clientes", response)


def obtener_cliente():
    cliente_id = _safe_int("ID cliente: ")
    response = requests.get(f"{BASE_URL}/clientes/{cliente_id}", timeout=10)
    _print_response(response)


def eliminar_cliente():
    cliente_id = _safe_int("ID cliente: ")
    response = requests.delete(f"{BASE_URL}/clientes/{cliente_id}", timeout=10)
    _print_response(response)


# Productos

def crear_producto():
    payload = {
        "nombre": input("Nombre producto: ").strip(),
        "precio": _safe_float("Precio: "),
        "stock": _safe_int("Stock: "),
    }
    response = requests.post(f"{BASE_URL}/productos", json=payload, timeout=10)
    _print_response(response)


def listar_productos():
    response = requests.get(f"{BASE_URL}/productos", timeout=10)
    _print_listado("Lista de productos", response)


def obtener_producto():
    producto_id = _safe_int("ID producto: ")
    response = requests.get(f"{BASE_URL}/productos/{producto_id}", timeout=10)
    _print_response(response)


def eliminar_producto():
    producto_id = _safe_int("ID producto: ")
    response = requests.delete(f"{BASE_URL}/productos/{producto_id}", timeout=10)
    _print_response(response)


# Pedidos

def crear_pedido():
    cliente_id = _safe_int("ID cliente: ")

    cantidad_items = _safe_int("Cuantos productos diferentes quieres agregar?: ")
    productos = []
    for i in range(cantidad_items):
        print(f"Producto #{i + 1}")
        producto_id = _safe_int("  ID producto: ")
        cantidad = _safe_int("  Cantidad: ")
        productos.append({"id": producto_id, "cantidad": cantidad})

    payload = {
        "cliente_id": cliente_id,
        "productos": productos,
    }
    response = requests.post(f"{BASE_URL}/pedidos", json=payload, timeout=10)
    _print_response(response)


def listar_pedidos():
    response = requests.get(f"{BASE_URL}/pedidos", timeout=10)
    _print_listado("Lista de pedidos", response)


def obtener_pedido():
    pedido_id = _safe_int("ID pedido: ")
    response = requests.get(f"{BASE_URL}/pedidos/{pedido_id}", timeout=10)
    _print_response(response)


def eliminar_pedido():
    pedido_id = _safe_int("ID pedido: ")
    response = requests.delete(f"{BASE_URL}/pedidos/{pedido_id}", timeout=10)
    _print_response(response)


def menu_clientes():
    while True:
        print("\n=== Clientes ===")
        print("1. Crear cliente")
        print("2. Listar clientes")
        print("3. Obtener cliente por ID")
        print("4. Eliminar cliente")
        print("0. Volver")
        opcion = _safe_int("Opcion: ")

        if opcion == 1:
            crear_cliente()
        elif opcion == 2:
            listar_clientes()
        elif opcion == 3:
            obtener_cliente()
        elif opcion == 4:
            eliminar_cliente()
        elif opcion == 0:
            break
        else:
            print("Opcion no valida.")


def menu_productos():
    while True:
        print("\n=== Productos ===")
        print("1. Crear producto")
        print("2. Listar productos")
        print("3. Obtener producto por ID")
        print("4. Eliminar producto")
        print("0. Volver")
        opcion = _safe_int("Opcion: ")

        if opcion == 1:
            crear_producto()
        elif opcion == 2:
            listar_productos()
        elif opcion == 3:
            obtener_producto()
        elif opcion == 4:
            eliminar_producto()
        elif opcion == 0:
            break
        else:
            print("Opcion no valida.")


def menu_pedidos():
    while True:
        print("\n=== Pedidos ===")
        print("1. Crear pedido")
        print("2. Listar pedidos")
        print("3. Obtener pedido por ID")
        print("4. Eliminar pedido")
        print("0. Volver")
        opcion = _safe_int("Opcion: ")

        if opcion == 1:
            crear_pedido()
        elif opcion == 2:
            listar_pedidos()
        elif opcion == 3:
            obtener_pedido()
        elif opcion == 4:
            eliminar_pedido()
        elif opcion == 0:
            break
        else:
            print("Opcion no valida.")


def main_menu():
    print("Cliente de Snack API")
    print("Asegurate de tener la API corriendo en http://127.0.0.1:8000")

    while True:
        print("\n=== Menu Principal ===")
        print("1. Clientes")
        print("2. Productos")
        print("3. Pedidos")
        print("0. Salir")
        opcion = _safe_int("Opcion: ")

        if opcion == 1:
            menu_clientes()
        elif opcion == 2:
            menu_productos()
        elif opcion == 3:
            menu_pedidos()
        elif opcion == 0:
            print("Saliendo...")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main_menu()
