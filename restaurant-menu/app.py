import psycopg
from psycopg import Error


def iniciar_conexion():
    try:
        conexion = psycopg.connect(
            host="localhost",
            port=5432,
            dbname="carta_digital",
            user="anderson",
            password="anderson2026",
            connect_timeout=5,
        )
        return conexion

    except Error as error:
        print(f"No fue posible conectarse a la base de datos: {error}")
        return None


def panel_opciones():
    validas = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    while True:
        opcion_seleccionada = input(
            "Seleccione la opcion deseada:\n\n"
            "1 - Ver carta completa\n"
            "2 - Filtrar productos por categoría\n"
            "3 - Buscar producto\n"
            "4 - Agregar producto\n"
            "5 - Modificar producto\n"
            "6 - Eliminar producto\n"
            "7 - Cambiar disponibilidad\n"
            "8 - Ver productos no disponibles\n"
            "9 - Ver estadísticas\n"
            "10 - Salir\n\n"
            "Respuesta: "
        ).strip()

        if opcion_seleccionada in validas:
            return opcion_seleccionada

        print("Opción inválida. Intente nuevamente.\n")


def pedir_valor():
    while True:
        valor = input("Ingrese el valor: ").strip()

        try:
            valor = float(valor)

            if valor > 0:
                return valor

            print("El valor debe ser mayor que 0.")

        except ValueError:
            print("Inválido. Ingrese un número válido.")


def agregar_producto(cursor, conexion):
    validas = ["1", "2", "3", "4"]

    tipo = input(
        "Ingrese el tipo del producto:\n"
        "1 - ENTRADA\n"
        "2 - PRINCIPAL\n"
        "3 - POSTRE\n"
        "4 - BEBIDA\n"
        "Respuesta: "
    ).strip()

    while tipo not in validas:
        tipo = input(
            "Inválido. Ingrese el tipo del producto:\n"
            "1 - ENTRADA\n"
            "2 - PRINCIPAL\n"
            "3 - POSTRE\n"
            "4 - BEBIDA\n"
            "Respuesta: "
        ).strip()

    nombre = input("Ingrese el nombre: ").strip().upper()
    while nombre == "":
        nombre = input("Inválido. Ingrese el nombre: ").strip().upper()

    valor = pedir_valor()

    tipos = {
        "1": "ENTRADA",
        "2": "PRINCIPAL",
        "3": "POSTRE",
        "4": "BEBIDA",
    }
    tipo = tipos[tipo]

    try:
        cursor.execute(
            "INSERT INTO productos (tipo, nombre, valor) VALUES (%s, %s, %s)",
            (tipo, nombre, valor),
        )
        conexion.commit()
        print("Producto agregado correctamente.\n")

    except Error as error:
        conexion.rollback()
        print(f"No fue posible agregar el producto: {error}\n")


def carta_completa(cursor):
    try:
        cursor.execute(
            "SELECT id, tipo, nombre, valor, disponible "
            "FROM productos WHERE disponible ORDER BY id"
        )
        productos = cursor.fetchall()

    except Error as error:
        print(f"No fue posible consultar la carta: {error}\n")
        return

    if not productos:
        print("No existen productos disponibles en la carta.\n")
        return

    categorias = [
        ("ENTRADA", "ENTRADAS"),
        ("PRINCIPAL", "PRINCIPALES"),
        ("POSTRE", "POSTRES"),
        ("BEBIDA", "BEBIDAS"),
    ]

    for categoria, titulo in categorias:
        productos_categoria = [
            producto for producto in productos if producto[1].upper() == categoria
        ]

        if productos_categoria:
            print(f"==== {titulo} ====\n")

            for id_prod, _, nombre, valor, _ in productos_categoria:
                print(f"ID: {id_prod}\n{nombre}\nPrecio: {valor}\n")


def filtrar_categoria(cursor):
    categorias = {
        "1": "ENTRADA",
        "2": "PRINCIPAL",
        "3": "POSTRE",
        "4": "BEBIDA",
    }

    filtro = input(
        "Seleccione la categoria para filtrar:\n"
        "1 - ENTRADA\n"
        "2 - PRINCIPAL\n"
        "3 - POSTRE\n"
        "4 - BEBIDA\n"
        "Respuesta: "
    ).strip()

    while filtro not in categorias:
        filtro = input("Opción inválida. Ingrese 1, 2, 3 o 4: ").strip()

    categoria = categorias[filtro]

    try:
        cursor.execute(
            "SELECT id, tipo, nombre, valor, disponible "
            "FROM productos WHERE UPPER(tipo) = %s AND disponible ORDER BY id",
            (categoria,),
        )
        productos = cursor.fetchall()

    except Error as error:
        print(f"No fue posible filtrar los productos: {error}\n")
        return

    if not productos:
        print("No existen productos disponibles en esta categoría.\n")
        return

    print(f"==== {categoria} ====\n")

    for id_prod, _, nombre, valor, _ in productos:
        print(f"ID: {id_prod}\n{nombre}\nPrecio: {valor}\n")


def manejo_opciones(opcion_seleccionada, conexion, cursor):
    while opcion_seleccionada != "10":
        match opcion_seleccionada:
            case "1":
                carta_completa(cursor)

            case "2":
                filtrar_categoria(cursor)

            case "3":
                print("En desarrollo.\n")

            case "4":
                agregar_producto(cursor, conexion)

            case "5" | "6" | "7" | "8" | "9":
                print("En desarrollo.\n")

        opcion_seleccionada = panel_opciones()

    print("Finalizando el programa...")


def main():
    conexion = iniciar_conexion()

    if conexion is None:
        return

    cursor = None

    try:
        cursor = conexion.cursor()
        opcion = panel_opciones()
        manejo_opciones(opcion, conexion, cursor)

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")

    except Error as error:
        print(f"Error de base de datos: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()


if __name__ == "__main__":
    main()
