from datetime import date
from peewee import ForeignKeyField, DateField, IntegerField
from prettytable import PrettyTable

from crud.operaciones import (
    crear_registro,
    listar_registros,
    buscar_registro,
    actualizar_registro,
    eliminar_registro,
)


def pedir_datos(modelo, registro=None):
    datos = {}

    for nombre, campo in modelo._meta.fields.items():
        if campo.primary_key:
            continue

        actual = getattr(registro, nombre) if registro else None

        if hasattr(actual, "get_id"):
            actual = actual.get_id()

        etiqueta = nombre.replace("_", " ").capitalize()
        obligatorio = not campo.null and campo.default is None

        while True:
            valor = input(
                f"{etiqueta}"
                + (f" [{actual}]" if actual is not None else "")
                + ": "
            ).strip()

            if not valor and registro is not None:
                break

            if not valor and not obligatorio:
                break

            if not valor and isinstance(campo, DateField):
                valor = date.today().isoformat()

            try:
                if isinstance(campo, ForeignKeyField):
                    datos[nombre] = int(valor)

                elif isinstance(campo, DateField):
                    datos[nombre] = date.fromisoformat(valor)

                elif isinstance(campo, IntegerField):
                    datos[nombre] = int(valor)

                else:
                    datos[nombre] = valor

                if nombre == "estado":
                    estados_validos = {
                        "PENDIENTE",
                        "EN_PROGRESO",
                        "COMPLETADA",
                        "BLOQUEADA",
                    }

                    if datos[nombre] not in estados_validos:
                        print(
                            "Estado inválido. Opciones: "
                            + ", ".join(sorted(estados_validos))
                        )
                        datos.pop(nombre)
                        continue

                break

            except ValueError:
                print("Valor inválido. Intenta nuevamente.")

    return datos


def menu_crud(modelo, nombre):
    while True:
        tabla = PrettyTable()
        tabla.field_names = ["Opción", f"Gestionar {nombre}"]

        opciones = [
            ("1", "Crear"),
            ("2", "Listar"),
            ("3", "Buscar"),
            ("4", "Actualizar"),
            ("5", "Eliminar"),
            ("0", "Volver"),
        ]

        for opcion, operacion in opciones:
            tabla.add_row([opcion, operacion])

        print(f"\n=== GESTIONAR {nombre.upper()} ===")
        print(tabla)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "0":
            break

        elif opcion == "1":
            datos = pedir_datos(modelo)

            if datos:
                crear_registro(modelo, datos)
            else:
                print("No se ingresaron datos.")

        elif opcion == "2":
            listar_registros(modelo)

        elif opcion == "3":
            identificador = input("ID del registro: ").strip()

            if identificador.isdigit():
                registro = buscar_registro(
                    modelo, int(identificador)
                )

                if registro:
                    print("\n=== DATOS DEL REGISTRO ===")
                    tabla = PrettyTable()
                    tabla.field_names = ["Campo", "Valor"]
                    for nombre, campo in modelo._meta.fields.items():
                        valor = getattr(registro, nombre)
                        if hasattr(valor, "get_id"):
                             valor = valor.get_id()
                        tabla.add_row([nombre, valor])
                    print(tabla)
            else:
                print("Ingresa un ID numérico válido.")

        elif opcion == "4":
            identificador = input("ID del registro: ").strip()

            if identificador.isdigit():
                registro = buscar_registro(
                    modelo, int(identificador)
                )

                if registro:
                    datos = pedir_datos(modelo, registro)

                    if datos:
                        actualizar_registro(
                            modelo,
                            int(identificador),
                            datos,
                        )
                    else:
                        print("No se modificaron campos.")
            else:
                print("Ingresa un ID numérico válido.")

        elif opcion == "5":
            identificador = input("ID del registro: ").strip()

            if identificador.isdigit():
                registro = buscar_registro(
                    modelo, int(identificador)
                )

                if registro:
                    print(registro)

                    confirmar = input(
                        "¿Eliminar? Escribe SI para confirmar: "
                    )

                    if confirmar.strip() == "SI":
                        eliminar_registro(
                            modelo,
                            int(identificador),
                        )
                    else:
                        print("Eliminación cancelada.")
            else:
                print("Ingresa un ID numérico válido.")

        else:
            if not opcion:
                print("Debes ingresar una opción.")
            else:
                print("Opción no válida.")

        input("\nPresiona Enter para continuar...")