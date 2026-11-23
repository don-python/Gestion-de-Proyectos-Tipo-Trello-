from prettytable import PrettyTable
from orm.models import (
    database, Proyecto, Tablero, Lista,
    Usuario, Tarjeta, Etiqueta, Comentario,
)

from crud.interfaz import menu_crud
from crud.proyecto_usuario import menu_participantes
from crud.tarjeta_etiqueta import menu_asociaciones
from crud.usuarios import buscar_usuario_por_rut  # importa búsqueda por RUT


# consola para buscar usuario por RUT desde el menú principal
def flujo_buscar_usuario_por_rut():
    print("\n--- BUSCAR USUARIO POR RUT ---")
    rut = input("Ingresa el RUT del usuario (ej. 12.345.678-9 o 12345678-9): ").strip()

    try:
        usuario = buscar_usuario_por_rut(rut)
    except ValueError as err:
        print(f"Error: {err}")
        return

    if not usuario:
        print("No se encontró ningún usuario con ese RUT.")
        return

    tabla = PrettyTable()
    tabla.field_names = ["ID", "RUT", "Nombre", "Email"]
    tabla.add_row([usuario.id, usuario.rut, usuario.nombre, usuario.email])
    print("\nUsuario encontrado:")
    print(tabla)


def mostrar_menu():
    tabla = PrettyTable()
    tabla.field_names = ["Opción", "Operación"]

    opciones = [
        ("1", "Listar proyectos"),
        ("2", "Listar tableros"),
        ("3", "Listar listas"),
        ("4", "Listar usuarios"),
        ("5", "Listar tarjetas"),
        ("6", "Listar etiquetas"),
        ("7", "Listar comentarios"),
        ("8", "Gestionar participantes de proyectos"),
        ("9", "Gestionar etiquetas de tarjetas"),
        ("10", "Buscar usuario por RUT"),  # [CAMBIO RUT]: nueva opción en el menú principal
        ("0", "Salir"),
    ]

    for opcion, operacion in opciones:
        tabla.add_row([opcion, operacion])

    print("\n=== GESTIÓN DE PROYECTOS ===")
    print(tabla)


def main():
    acciones = {
        "1": lambda: menu_crud(Proyecto, "Proyectos"),
        "2": lambda: menu_crud(Tablero, "Tableros"),
        "3": lambda: menu_crud(Lista, "Listas"),
        "4": lambda: menu_crud(Usuario, "Usuarios"),
        "5": lambda: menu_crud(Tarjeta, "Tarjetas"),
        "6": lambda: menu_crud(Etiqueta, "Etiquetas"),
        "7": lambda: menu_crud(Comentario, "Comentarios"),
        "8": menu_participantes,
        "9": menu_asociaciones,
        "10": flujo_buscar_usuario_por_rut,  # [CAMBIO RUT]: asocia la opción 10 a la búsqueda por RUT
    }

    try:
        while True:
            mostrar_menu()
            opcion = input("Selecciona una opción: ").strip()

            if opcion == "0":
                print("Hasta pronto.")
                break

            accion = acciones.get(opcion)

            if accion:
                accion()
                input("\nPresiona Enter para continuar...")
            else:
                print("Opción no válida.")

    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado.")

    finally:
        if not database.is_closed():
            database.close()


if __name__ == "__main__":
    main()