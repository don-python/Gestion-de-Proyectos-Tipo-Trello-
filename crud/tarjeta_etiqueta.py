
from peewee import IntegrityError
from orm.models import TarjetaEtiqueta
from prettytable import PrettyTable

def listar_asociaciones():
    try:
        with TarjetaEtiqueta._meta.database.connection_context():
            registros = list(TarjetaEtiqueta.select())

        if not registros:
            print("No hay etiquetas asociadas a tarjetas.")
            return []

        for registro in registros:
            print(
                f"Tarjeta ID: {registro.tarjeta_id} | "
                f"Etiqueta ID: {registro.etiqueta_id}"
            )

        return registros

    except Exception as error:
        print(f"Error al listar asociaciones: {error}")
        return []


def asociar_etiqueta(tarjeta_id, etiqueta_id):
    try:
        with TarjetaEtiqueta._meta.database.connection_context():
            TarjetaEtiqueta.create(
                tarjeta=tarjeta_id,
                etiqueta=etiqueta_id
            )

        print("Etiqueta asociada correctamente.")
        return True

    except IntegrityError:
        print(
            "No se pudo asociar. Comprueba que existan la tarjeta "
            "y la etiqueta, y que la asociación no esté duplicada."
        )
        return False

    except Exception as error:
        print(f"Error al asociar etiqueta: {error}")
        return False


def desasociar_etiqueta(tarjeta_id, etiqueta_id):
    try:
        with TarjetaEtiqueta._meta.database.connection_context():
            consulta = TarjetaEtiqueta.delete().where(
                (TarjetaEtiqueta.tarjeta == tarjeta_id) &
                (TarjetaEtiqueta.etiqueta == etiqueta_id)
            )
            eliminados = consulta.execute()

        if eliminados:
            print("Etiqueta desasociada correctamente.")
            return True

        print("No se encontró esa asociación.")
        return False

    except Exception as error:
        print(f"Error al desasociar etiqueta: {error}")
        return False

def menu_asociaciones():
    while True:
        tabla = PrettyTable()
        tabla.field_names = ["Opción", "Operación"]
        tabla.add_rows([
            ["1", "Listar asociaciones"],
            ["2", "Asociar etiqueta a tarjeta"],
            ["3", "Desasociar etiqueta de tarjeta"],
            ["0", "Volver"]
        ])

        print("\n=== GESTIÓN DE ETIQUETAS DE TARJETAS ===")
        print(tabla)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            listar_asociaciones()

        elif opcion == "2":
            tarjeta_id = input("ID de la tarjeta: ").strip()
            etiqueta_id = input("ID de la etiqueta: ").strip()

            if tarjeta_id.isdigit() and etiqueta_id.isdigit():
                asociar_etiqueta(
                    int(tarjeta_id),
                    int(etiqueta_id)
                )
            else:
                print("Debes ingresar ID numéricos válidos.")

        elif opcion == "3":
            tarjeta_id = input("ID de la tarjeta: ").strip()
            etiqueta_id = input("ID de la etiqueta: ").strip()

            if tarjeta_id.isdigit() and etiqueta_id.isdigit():
                desasociar_etiqueta(
                    int(tarjeta_id),
                    int(etiqueta_id)
                )
            else:
                print("Debes ingresar ID numéricos válidos.")

        elif opcion == "0":
            break

        else:
            print("Opción no válida.")

        input("\nPresiona Enter para continuar...")
