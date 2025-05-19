import sqlite3
from colorama import Fore, Style, init

# Inicializar colorama para colores en la terminal
init(autoreset=True)


# Función para conectar a la base de datos
def conectar():
    return sqlite3.connect("inventario.db")


# Función para registrar un nuevo producto
def registrar_producto():
    print(Fore.CYAN + "\n--- Registrar Nuevo Producto ---")
    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()
    while True:
        cantidad = input("Cantidad: ").strip()
        if cantidad.isdigit():
            cantidad = int(cantidad)
            break
        print(Fore.RED + "Cantidad inválida. Debe ser un número entero.")
    while True:
        try:
            precio = float(input("Precio: ").strip())
            break
        except ValueError:
            print(Fore.RED + "Precio inválido. Debe ser un número.")
    categoria = input("Categoría: ").strip()
    with conectar() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
            (nombre, descripcion, cantidad, precio, categoria),
        )
        print(Fore.GREEN + "Producto registrado exitosamente.")


# Función para mostrar todos los productos
def mostrar_productos():
    print(Fore.CYAN + "\n--- Lista de Productos ---")
    with conectar() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM productos")
        productos = cur.fetchall()
        if productos:
            for p in productos:
                print(
                    Fore.YELLOW
                    + f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}"
                )
        else:
            print(Fore.RED + "No hay productos registrados.")


# Función para buscar productos por ID, nombre o categoría
def buscar_producto():
    print(Fore.CYAN + "\n--- Buscar Producto ---")
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    print("3. Buscar por categoría")
    opcion_busqueda = input("Seleccione una opción de búsqueda (1-3): ").strip()

    with conectar() as con:
        cur = con.cursor()
        if opcion_busqueda == "1":
            id_buscar = input("Ingrese el ID del producto a buscar: ").strip()
            if not id_buscar.isdigit():
                print(Fore.RED + "ID inválido.")
                return
            cur.execute("SELECT * FROM productos WHERE id = ?", (int(id_buscar),))
            p = cur.fetchone()
            if p:
                print(
                    Fore.YELLOW
                    + f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}"
                )
            else:
                print(Fore.RED + "No se encontró un producto con ese ID.")

        elif opcion_busqueda == "2":
            nombre_buscar = input(
                "Ingrese el nombre (o parte) del producto a buscar: "
            ).strip()
            if not nombre_buscar:
                print(Fore.RED + "Debe ingresar un nombre.")
                return
            cur.execute(
                "SELECT * FROM productos WHERE LOWER(nombre) LIKE ?",
                ("%" + nombre_buscar.lower() + "%",),
            )
            productos = cur.fetchall()
            if productos:
                print(Fore.CYAN + "\n--- Resultados de la búsqueda por nombre ---")
                for p in productos:
                    print(
                        Fore.YELLOW
                        + f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}"
                    )
            else:
                print(Fore.RED + "No se encontraron productos con ese nombre.")

        elif opcion_busqueda == "3":
            categoria_buscar = input(
                "Ingrese la categoría (o parte) a buscar: "
            ).strip()
            if not categoria_buscar:
                print(Fore.RED + "Debe ingresar una categoría.")
                return
            cur.execute(
                "SELECT * FROM productos WHERE LOWER(categoria) LIKE ?",
                ("%" + categoria_buscar.lower() + "%",),
            )
            productos = cur.fetchall()
            if productos:
                print(Fore.CYAN + "\n--- Resultados de la búsqueda por categoría ---")
                for p in productos:
                    print(
                        Fore.YELLOW
                        + f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}"
                    )
            else:
                print(Fore.RED + "No se encontraron productos en esa categoría.")
        else:
            print(Fore.RED + "Opción de búsqueda no válida.")


# Función para actualizar un producto por ID
def actualizar_producto():
    print(Fore.CYAN + "\n--- Actualizar Producto ---")
    id_actualizar = input("Ingrese el ID del producto a actualizar: ").strip()
    if not id_actualizar.isdigit():
        print(Fore.RED + "ID inválido.")
        return
    with conectar() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM productos WHERE id = ?", (int(id_actualizar),))
        p = cur.fetchone()
        if not p:
            print(Fore.RED + "No se encontró un producto con ese ID.")
            return
        print(
            Fore.YELLOW
            + f"Producto actual: Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: {p[4]}, Categoría: {p[5]}"
        )
        nombre = input("Nuevo nombre (Enter para mantener): ").strip() or p[1]
        descripcion = input("Nueva descripción (Enter para mantener): ").strip() or p[2]
        cantidad = input("Nueva cantidad (Enter para mantener): ").strip()
        cantidad = int(cantidad) if cantidad.isdigit() else p[3]
        precio = input("Nuevo precio (Enter para mantener): ").strip()
        try:
            precio = float(precio) if precio else p[4]
        except ValueError:
            precio = p[4]
        categoria = input("Nueva categoría (Enter para mantener): ").strip() or p[5]
        cur.execute(
            "UPDATE productos SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=? WHERE id=?",
            (nombre, descripcion, cantidad, precio, categoria, int(id_actualizar)),
        )
        print(Fore.GREEN + "Producto actualizado exitosamente.")


# Función para eliminar un producto por ID
def eliminar_producto():
    print(Fore.CYAN + "\n--- Eliminar Producto ---")
    id_eliminar = input("Ingrese el ID del producto a eliminar: ").strip()
    if not id_eliminar.isdigit():
        print(Fore.RED + "ID inválido.")
        return
    with conectar() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM productos WHERE id = ?", (int(id_eliminar),))
        if cur.rowcount:
            print(Fore.GREEN + "Producto eliminado exitosamente.")
        else:
            print(Fore.RED + "No se encontró un producto con ese ID.")


# Función para mostrar productos con bajo stock
def reporte_bajo_stock():
    print(Fore.CYAN + "\n--- Reporte de Bajo Stock ---")
    limite = input("Mostrar productos con cantidad igual o menor a: ").strip()
    if not limite.isdigit():
        print(Fore.RED + "Límite inválido.")
        return
    with conectar() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM productos WHERE cantidad <= ?", (int(limite),))
        productos = cur.fetchall()
        if productos:
            for p in productos:
                print(Fore.YELLOW + f"ID: {p[0]}, Nombre: {p[1]}, Cantidad: {p[3]}")
        else:
            print(Fore.RED + "No hay productos con bajo stock.")


# Crear la tabla 'productos' si no existe
with conectar() as con:
    cur = con.cursor()
    cur.execute(
        """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT
)
"""
    )

print(
    Fore.GREEN + "Base de datos 'inventario.db' y tabla 'productos' listas para usar."
)

# Menú principal de la aplicación
while True:
    print(Style.BRIGHT + Fore.BLUE + "\n===== Menú de Inventario =====")
    print(Fore.YELLOW + "1. Agregar producto")
    print(Fore.YELLOW + "2. Mostrar productos")
    print(Fore.YELLOW + "3. Buscar producto")
    print(Fore.YELLOW + "4. Actualizar producto por ID")
    print(Fore.YELLOW + "5. Eliminar producto por ID")
    print(Fore.YELLOW + "6. Reporte de bajo stock")
    print(Fore.YELLOW + "7. Salir")
    print(Style.RESET_ALL)
    opcion = input(Fore.CYAN + "Seleccione una opción (1-7): ").strip()

    if opcion == "1":
        registrar_producto()
    elif opcion == "2":
        mostrar_productos()
    elif opcion == "3":
        buscar_producto()
    elif opcion == "4":
        actualizar_producto()
    elif opcion == "5":
        eliminar_producto()
    elif opcion == "6":
        reporte_bajo_stock()
    elif opcion == "7":
        print(Fore.BLUE + "Saliendo del sistema. ¡Hasta luego!")
        break
    else:
        print(Fore.RED + "Opción no válida. Intente nuevamente.")
