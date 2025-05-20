# TFI_Com25006

Trabajo Final Integrador: Gestor de Inventario

## Descripción

Este proyecto es una aplicación de consola desarrollada en Python para la gestión de inventario de productos. Permite registrar, consultar, actualizar, eliminar y reportar productos almacenados en una base de datos SQLite llamada `inventario.db`. Utiliza la librería `colorama` para mejorar la visualización de mensajes en la terminal con colores.

## ¿Cómo funciona el programa?

Al ejecutar el archivo [`tfi.py`](tfi.py), el sistema crea automáticamente la base de datos y la tabla de productos si no existen. Luego, muestra un menú interactivo donde el usuario puede elegir entre las siguientes opciones:

1. **Agregar producto:** Permite ingresar los datos de un nuevo producto (nombre, descripción, cantidad, precio y categoría) y guardarlo en la base de datos.
2. **Mostrar productos:** Lista todos los productos registrados mostrando sus datos principales.
3. **Buscar producto:** Permite buscar productos por ID, nombre o categoría.
4. **Actualizar producto por ID:** Permite modificar los datos de un producto existente, identificándolo por su ID.
5. **Eliminar producto por ID:** Elimina un producto de la base de datos usando su ID.
6. **Reporte de bajo stock:** Muestra los productos cuya cantidad es igual o menor a un valor ingresado por el usuario.
7. **Salir:** Finaliza el programa.

## Lógica utilizada

- **Persistencia:** Se utiliza SQLite para almacenar los productos en la base de datos `inventario.db`.
- **Interfaz de usuario:** El menú y las opciones se presentan en la terminal. El usuario interactúa mediante la introducción de números y textos.
- **Validaciones:** Se valida que los campos numéricos (cantidad, precio, ID) sean correctos antes de realizar operaciones.
- **Colores:** Se emplea `colorama` para diferenciar mensajes de éxito, error y advertencia.

## Variables y funciones principales

- **conectar():** Función que retorna una conexión a la base de datos.
- **registrar_producto():** Solicita los datos del producto y los inserta en la base de datos.
  - Variables: `nombre`, `descripcion`, `cantidad`, `precio`, `categoria`
- **mostrar_productos():** Recupera y muestra todos los productos.
- **buscar_producto():** Permite buscar productos por ID, nombre o categoría.
  - Variables: `opcion_busqueda`, `id_buscar`, `nombre_buscar`, `categoria_buscar`
- **actualizar_producto():** Permite modificar los datos de un producto existente.
  - Variables: `id_actualizar`, `nombre`, `descripcion`, `cantidad`, `precio`, `categoria`
- **eliminar_producto():** Elimina un producto por su ID.
  - Variable: `id_eliminar`
- **reporte_bajo_stock():** Muestra productos con cantidad baja.
  - Variable: `limite`

## Estructura de la base de datos

La tabla `productos` contiene los siguientes campos:

- `id`: INTEGER, clave primaria autoincremental
- `nombre`: TEXT, nombre del producto
- `descripcion`: TEXT, descripción del producto
- `cantidad`: INTEGER, cantidad disponible
- `precio`: REAL, precio unitario
- `categoria`: TEXT, categoría del producto

## Requisitos

- Python 3.x
- Paquete `colorama` (instalar con `pip install colorama`)

## Ejecución

Desde la terminal, navega a la carpeta `TFI_Com25006` y ejecuta:

```sh
python tfi.py
```
