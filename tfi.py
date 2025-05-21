import sqlite3
from colorama import Fore, Style, init

# Inicializar colorama para colores en la terminal
init(autoreset=True)


# Función para conectar a la base de datos
def conectar():
    try:
        return sqlite3.connect("inventario.db")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error de conexión a la base de datos: {e}")
        return None


# Función para registrar un nuevo producto
def registrar_producto():
    print(Fore.CYAN + "\n--- Registrar Nuevo Producto ---")
    # Validar nombre no vacío
    while True:
        nombre = input("Nombre: ").strip()
        if nombre:
            break
        print(Fore.RED + "El nombre no puede estar vacío.")
    # Validar descripción no vacía
    while True:
        descripcion = input("Descripción: ").strip()
        if descripcion:
            break
        print(Fore.RED + "La descripción no puede estar vacía.")
    # Validar cantidad (no permitir valores negativos)
    while True:
        cantidad = input("Cantidad: ").strip()
        if cantidad.isdigit() and int(cantidad) >= 0:
            cantidad = int(cantidad)
            break
        print(Fore.RED + "Cantidad inválida. Debe ser un número entero no negativo.")
    # Validar precio no negativo
    while True:
        try:
            precio = float(input("Precio: ").strip())
            if precio < 0:
                print(Fore.RED + "El precio no puede ser negativo.")
            else:
                break
        except ValueError:
            print(Fore.RED + "Precio inválido. Debe ser un número.")
    # Validar categoría no vacía
    while True:
        categoria = input("Categoría: ").strip()
        if categoria:
            break
        print(Fore.RED + "La categoría no puede estar vacía.")
    con = conectar()
    if con is None:
        return
    try:
        with con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                (nombre, descripcion, cantidad, precio, categoria),
            )
            print(Fore.GREEN + "Producto registrado exitosamente.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al registrar producto: {e}")


# Función para mostrar todos los productos
def mostrar_productos():
    print(Fore.CYAN + "\n--- Lista de Productos ---")
    con = conectar()
    if con is None:
        return
    try:
        with con:
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
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al mostrar productos: {e}")


# Función para buscar productos por ID, nombre o categoría
def buscar_producto():
    print(Fore.CYAN + "\n--- Buscar Producto ---")
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    print("3. Buscar por categoría")
    opcion_busqueda = input("Seleccione una opción de búsqueda (1-3): ").strip()

    con = conectar()
    if con is None:
        return
    try:
        with con:
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
                    print(
                        Fore.CYAN + "\n--- Resultados de la búsqueda por categoría ---"
                    )
                    for p in productos:
                        print(
                            Fore.YELLOW
                            + f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}"
                        )
                else:
                    print(Fore.RED + "No se encontraron productos en esa categoría.")
            else:
                print(Fore.RED + "Opción de búsqueda no válida.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al buscar productos: {e}")


# Función para actualizar un producto por ID
def actualizar_producto():
    print(Fore.CYAN + "\n--- Actualizar Producto ---")
    id_actualizar = input("Ingrese el ID del producto a actualizar: ").strip()
    if not id_actualizar.isdigit():
        print(Fore.RED + "ID inválido.")
        return
    con = conectar()
    if con is None:
        return
    try:
        with con:
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
            # Validar nombre no vacío
            while True:
                nombre = input("Nuevo nombre (Enter para mantener): ").strip()
                if nombre == "":
                    nombre = p[1]
                if nombre:
                    break
                print(Fore.RED + "El nombre no puede estar vacío.")
            # Validar descripción no vacía
            while True:
                descripcion = input("Nueva descripción (Enter para mantener): ").strip()
                if descripcion == "":
                    descripcion = p[2]
                if descripcion:
                    break
                print(Fore.RED + "La descripción no puede estar vacía.")
            # Validación para cantidad (no permitir valores negativos)
            while True:
                cantidad = input("Nueva cantidad (Enter para mantener): ").strip()
                if cantidad == "":
                    cantidad = p[3]
                    break
                elif cantidad.isdigit() and int(cantidad) >= 0:
                    cantidad = int(cantidad)
                    break
                else:
                    print(
                        Fore.RED
                        + "Cantidad inválida. Debe ser un número entero no negativo."
                    )
            # Validación para precio no negativo
            while True:
                precio = input("Nuevo precio (Enter para mantener): ").strip()
                if precio == "":
                    precio = p[4]
                    break
                try:
                    precio = float(precio)
                    if precio < 0:
                        print(Fore.RED + "El precio no puede ser negativo.")
                    else:
                        break
                except ValueError:
                    print(Fore.RED + "Precio inválido. Debe ser un número.")
            # Validar categoría no vacía
            while True:
                categoria = input("Nueva categoría (Enter para mantener): ").strip()
                if categoria == "":
                    categoria = p[5]
                if categoria:
                    break
                print(Fore.RED + "La categoría no puede estar vacía.")
            cur.execute(
                "UPDATE productos SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=? WHERE id=?",
                (nombre, descripcion, cantidad, precio, categoria, int(id_actualizar)),
            )
            print(Fore.GREEN + "Producto actualizado exitosamente.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al actualizar producto: {e}")


# Función para eliminar un producto por ID
def eliminar_producto():
    print(Fore.CYAN + "\n--- Eliminar Producto ---")
    id_eliminar = input("Ingrese el ID del producto a eliminar: ").strip()
    if not id_eliminar.isdigit():
        print(Fore.RED + "ID inválido.")
        return
    con = conectar()
    if con is None:
        return
    try:
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM productos WHERE id = ?", (int(id_eliminar),))
            if cur.rowcount:
                print(Fore.GREEN + "Producto eliminado exitosamente.")
            else:
                print(Fore.RED + "No se encontró un producto con ese ID.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al eliminar producto: {e}")


# Función para mostrar productos con bajo stock
def reporte_bajo_stock():
    print(Fore.CYAN + "\n--- Reporte de Bajo Stock ---")
    limite = input("Mostrar productos con cantidad igual o menor a: ").strip()
    if not limite.isdigit():
        print(Fore.RED + "Límite inválido.")
        return
    con = conectar()
    if con is None:
        return
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM productos WHERE cantidad <= ?", (int(limite),))
            productos = cur.fetchall()
            if productos:
                for p in productos:
                    print(Fore.YELLOW + f"ID: {p[0]}, Nombre: {p[1]}, Cantidad: {p[3]}")
            else:
                print(Fore.RED + "No hay productos con bajo stock.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al generar el reporte: {e}")


# Crear la tabla 'productos' si no existe
con = conectar()
if con is not None:
    try:
        with con:
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
            Fore.GREEN
            + "Base de datos 'inventario.db' y tabla 'productos' listas para usar."
        )
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al crear la tabla: {e}")
else:
    print(Fore.RED + "No se pudo inicializar la base de datos.")

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
