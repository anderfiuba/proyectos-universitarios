import psycopg


def iniciar_conexion():
    print("Intentando conectar...")

    conexion = psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname="tienda",
        user="anderson",
        password="Anderson2026",
        connect_timeout=5
    )

    print("Conectado.")
    return conexion


def manejo_err(cod):

    if cod == "id":
        while True:
            try:
                usr_input = int(input("Ingrese un ID válido: "))

                if usr_input > 0:
                    return usr_input

                print("El ID debe ser mayor a 0.")

            except ValueError:
                print("Debe ingresar un número.")


    elif cod == "nombre":
        usr_input = input(
            "Ingrese el nombre del producto: "
        ).strip().upper()

        while usr_input == "":
            usr_input = input(
                "Inválido. Ingrese el nombre del producto: "
            ).strip().upper()

        return usr_input


    elif cod == "precio":
        while True:
            try:
                usr_input = int(
                    input("Ingrese el valor del producto: ")
                )

                if usr_input > 0:
                    return usr_input

                print("El precio debe ser mayor a 0.")

            except ValueError:
                print("Debe ingresar un número.")


    elif cod == "stock":
        while True:
            try:
                usr_input = int(
                    input("Ingrese el stock del producto: ")
                )

                if usr_input >= 0:
                    return usr_input

                print("El stock no puede ser negativo.")

            except ValueError:
                print("Debe ingresar un número.")


def mostrar_productos(cursor):
    cursor.execute(
        "SELECT id, nombre, precio, stock "
        "FROM productos ORDER BY id"
    )

    productos = cursor.fetchall()

    if not productos:
        print("No hay productos cargados.")
        return

    print("\n--- PRODUCTOS ---")

    for producto in productos:
        id_producto, nombre, precio, stock = producto

        if stock < 5:
            print(
                f"{id_producto} | {nombre} | "
                f"${precio} | Stock: {stock} | STOCK BAJO"
            )
        else:
            print(
                f"{id_producto} | {nombre} | "
                f"${precio} | Stock: {stock}"
            )


def buscar_producto(cursor):
    usr_producto = manejo_err("nombre")

    cursor.execute(
        "SELECT id, nombre, precio, stock "
        "FROM productos "
        "WHERE UPPER(nombre) = %s",
        (usr_producto,)
    )

    productos = cursor.fetchall()

    if not productos:
        print("Producto no encontrado.")
        return

    for producto in productos:
        id_producto, nombre, precio, stock = producto

        print(
            f"{id_producto} | {nombre} | "
            f"${precio} | Stock: {stock}"
        )


def agregar_producto(cursor, conexion):
    usr_nombre = manejo_err("nombre")
    usr_precio = manejo_err("precio")
    usr_stock = manejo_err("stock")

    cursor.execute(
        "INSERT INTO productos "
        "(nombre, precio, stock) "
        "VALUES (%s, %s, %s)",
        (usr_nombre, usr_precio, usr_stock)
    )

    conexion.commit()

    print("Producto agregado correctamente.")


def actualizar_producto(cursor, conexion):
    usr_id = manejo_err("id")
    usr_stock = manejo_err("stock")

    cursor.execute(
        "UPDATE productos "
        "SET stock = %s "
        "WHERE id = %s",
        (usr_stock, usr_id)
    )

    if cursor.rowcount == 0:
        print("Producto no encontrado.")
        return

    conexion.commit()

    print(
        f"Stock del producto {usr_id} "
        f"actualizado a {usr_stock}."
    )


def eliminar_producto(cursor, conexion):
    usr_id = manejo_err("id")

    cursor.execute(
        "DELETE FROM productos WHERE id = %s",
        (usr_id,)
    )

    if cursor.rowcount == 0:
        print("Producto no encontrado.")
        return

    conexion.commit()

    print("Producto eliminado correctamente.")


def main():
    conexion = iniciar_conexion()
    cursor = conexion.cursor()

    opcion = ""

    while opcion != "6":

        opcion = input(
            "\n--- CONTROL DE STOCK ---\n"
            "1 - Ver productos\n"
            "2 - Buscar producto\n"
            "3 - Agregar producto\n"
            "4 - Actualizar stock\n"
            "5 - Eliminar producto\n"
            "6 - Salir\n"
            "Seleccione una opción: "
        )

        match opcion:

            case "1":
                mostrar_productos(cursor)

            case "2":
                buscar_producto(cursor)

            case "3":
                agregar_producto(cursor, conexion)

            case "4":
                actualizar_producto(cursor, conexion)

            case "5":
                eliminar_producto(cursor, conexion)

            case "6":
                print("Programa finalizado.")

            case _:
                print("Opción inválida.")

    cursor.close()
    conexion.close()


main()
