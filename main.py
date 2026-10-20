from prettytable import PrettyTable
from orm.models import (
    database, Proyecto, Tablero, Lista,
    Usuario, Tarjeta, Etiqueta, Comentario,
)

from crud.interfaz import menu_crud
from crud.proyecto_usuario import menu_participantes
from crud.tarjeta_etiqueta import menu_asociaciones



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
