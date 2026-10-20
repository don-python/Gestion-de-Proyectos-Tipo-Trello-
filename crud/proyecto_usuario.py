
from peewee import IntegrityError
from orm.models import ProyectoUsuario
from prettytable import PrettyTable

def listar_participantes():
    try:
        with ProyectoUsuario._meta.database.connection_context():
            registros = list(ProyectoUsuario.select())

        if not registros:
            print("No hay participantes registrados.")
            return []

        for registro in registros:
            print(
                f"Proyecto ID: {registro.proyecto_id} | "
                f"Usuario ID: {registro.usuario_id}"
            )

        return registros

    except Exception as error:
        print(f"Error al listar participantes: {error}")
        return []


def agregar_participante(proyecto_id, usuario_id):
    try:
        with ProyectoUsuario._meta.database.connection_context():
            ProyectoUsuario.create(
                proyecto=proyecto_id,
                usuario=usuario_id
            )

        print("Participante agregado correctamente.")
        return True

    except IntegrityError:
        print(
            "No se pudo agregar. Comprueba que existan el proyecto "
            "y el usuario, y que la relación no esté duplicada."
        )
        return False

    except Exception as error:
        print(f"Error al agregar participante: {error}")
        return False


def eliminar_participante(proyecto_id, usuario_id):
    try:
        with ProyectoUsuario._meta.database.connection_context():
            consulta = ProyectoUsuario.delete().where(
                (ProyectoUsuario.proyecto == proyecto_id) &
                (ProyectoUsuario.usuario == usuario_id)
            )
            eliminados = consulta.execute()

        if eliminados:
            print("Participante eliminado correctamente.")
            return True

        print("No se encontró esa relación.")
        return False

    except Exception as error:
        print(f"Error al eliminar participante: {error}")
        return False

def menu_participantes():
    while True:
        tabla = PrettyTable()
        tabla.field_names = ["Opción", "Operación"]
        tabla.add_rows([
            ["1", "Listar participantes"],
            ["2", "Agregar participante"],
            ["3", "Eliminar participante"],
            ["0", "Volver"]
        ])

        print("\n=== GESTIÓN DE PARTICIPANTES ===")
        print(tabla)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            listar_participantes()

        elif opcion == "2":
            proyecto_id = input("ID del proyecto: ").strip()
            usuario_id = input("ID del usuario: ").strip()

            if proyecto_id.isdigit() and usuario_id.isdigit():
                agregar_participante(
                    int(proyecto_id),
                    int(usuario_id)
                )
            else:
                print("Debes ingresar ID numéricos válidos.")

        elif opcion == "3":
            proyecto_id = input("ID del proyecto: ").strip()
            usuario_id = input("ID del usuario: ").strip()

            if proyecto_id.isdigit() and usuario_id.isdigit():
                eliminar_participante(
                    int(proyecto_id),
                    int(usuario_id)
                )
            else:
                print("Debes ingresar ID numéricos válidos.")

        elif opcion == "0":
            break

        else:
            print("Opción no válida.")

        input("\nPresiona Enter para continuar...")
