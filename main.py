
from orm.models import database
from prettytable import PrettyTable


def mostrar_menu():
    tabla = PrettyTable()
    tabla.field_names = ["Opción", "Operación"]

    opciones = [
        ("1", "Gestionar proyectos"),
        ("2", "Gestionar tableros"),
        ("3", "Gestionar listas"),
        ("4", "Gestionar usuarios"),
        ("5", "Gestionar tarjetas"),
        ("6", "Gestionar etiquetas"),
        ("7", "Gestionar comentarios"),
        ("8", "Gestionar participantes de proyectos"),
        ("9", "Gestionar etiquetas de tarjetas"),
        ("0", "Salir")
    ]

    for opcion, operacion in opciones:
        tabla.add_row([opcion, operacion])

    print("\nGestión de proyectos")
    print(tabla)


def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "0":
            print("Hasta pronto.")
            break
        elif opcion in [str(i) for i in range(1, 10)]:
            print("Sección seleccionada:", opcion)
            print("Esta sección se implementará en el siguiente paso.")
            input("\nPresiona Enter para continuar...")
        else:
            print("Opción no válida.")

    database.close()


if __name__ == "__main__":
    main()
