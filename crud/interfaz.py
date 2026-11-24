from datetime import date
import maskpass
from peewee import ForeignKeyField, DateField, IntegerField, IntegrityError
from prettytable import PrettyTable

from orm.models import Usuario, normalizar_rut, validar_rut, validar_email, validar_password
from crud.operaciones import (
    crear_registro,
    listar_registros,
    buscar_registro,
    actualizar_registro,
    eliminar_registro,
)
from crud.usuarios import crear_usuario, actualizar_usuario, buscar_usuario_por_rut  # CRUD usuario


# helper para mostrar en tabla los campos de cualquier registro encontrado
def _mostrar_detalle_registro(modelo, registro):
    print("\n=== DATOS DEL REGISTRO ===")
    tabla = PrettyTable()
    tabla.field_names = ["Campo", "Valor"]
    for campo_nombre in modelo._meta.fields.keys():
        if modelo is Usuario and campo_nombre == "password":
            continue
        valor = getattr(registro, campo_nombre)
        if hasattr(valor, "get_id"):
            valor = valor.get_id()
        tabla.add_row([campo_nombre, valor])
    print(tabla)


def pedir_datos(modelo, registro=None):
    datos = {}

    for nombre, campo in modelo._meta.fields.items():
        if campo.primary_key:
            continue

        actual = getattr(registro, nombre) if registro else None

        if modelo is Usuario and nombre == "password":
            actual = None

        if hasattr(actual, "get_id"):
            actual = actual.get_id()

        etiqueta = nombre.replace("_", " ").capitalize()
        obligatorio = not campo.null and campo.default is None

        while True:
            prompt = (
                f"{etiqueta}"
                + (f" [{actual}]" if actual is not None else "")
                + ": "
            )
            if modelo is Usuario and nombre == "password":
                valor = maskpass.askpass(prompt=prompt, mask="*").strip()
            else:
                valor = input(prompt).strip()

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

                elif modelo is Usuario and nombre == "password":
                    if not validar_password(valor):
                        print(
                            "Contraseña débil. Debe tener al menos 8 caracteres, "
                            "una mayúscula, un número y un símbolo."
                        )
                        continue
                    datos[nombre] = valor

                elif modelo is Usuario and nombre == "email":
                    if not validar_email(valor):
                        print("Correo inválido. Usa un formato como nombre@dominio.cl.")
                        continue
                    datos[nombre] = valor

                # valida formato/DV y comprueba que el RUT no esté repetido al pedir datos de Usuario
                elif modelo is Usuario and nombre == "rut":
                    if not validar_rut(valor):
                        print("RUT inválido. Verifica el número y el dígito verificador (ej. 12.345.678-9).")
                        continue

                    rut_norm = normalizar_rut(valor)
                    consulta = Usuario.select().where(Usuario.rut == rut_norm)
                    if registro is not None:
                        consulta = consulta.where(Usuario.id != registro.id)

                    if consulta.exists():
                        print(f"El RUT {rut_norm} ya está registrado en otro usuario. Ingresa uno distinto.")
                        continue

                    datos[nombre] = rut_norm

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

            except ValueError as err:  # mensaje por si falla el RUT
                if modelo is Usuario and nombre == "rut":
                    print(f"Error de RUT: {err}")
                else:
                    print("Valor inválido. Intenta nuevamente.")

    return datos


# permite elegir buscar un usuario por ID o por RUT
def _buscar_usuario_interactivo():
    print("\nBuscar usuario por:")
    print("1. ID")
    print("2. RUT")
    criterio = input("Selecciona una opción: ").strip()

    if criterio == "1":
        identificador = input("ID del usuario: ").strip()
        if identificador.isdigit():
            return buscar_registro(Usuario, int(identificador))
        print("Ingresa un ID numérico válido.")
        return None

    if criterio == "2":
        rut = input("RUT del usuario (ej. 12.345.678-9 o 12345678-9): ").strip()
        try:
            usuario = buscar_usuario_por_rut(rut)
            if not usuario:
                print("No se encontró ningún usuario con ese RUT.")
            return usuario
        except ValueError as err:
            print(f"Error: {err}")
            return None

    print("Opción de búsqueda no válida.")
    return None


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
                # usa crear_usuario y captura errores de validación o duplicado
                try:
                    if modelo is Usuario:
                        crear_usuario(datos)
                    else:
                        crear_registro(modelo, datos)
                except (ValueError, IntegrityError) as err:
                    print(f"No se pudo crear el registro: {err}")
            else:
                print("No se ingresaron datos.")

        elif opcion == "2":
            listar_registros(modelo)

        elif opcion == "3":
            # redirige a búsqueda por ID o RUT cuando el modelo es Usuario
            if modelo is Usuario:
                registro = _buscar_usuario_interactivo()
                if registro:
                    _mostrar_detalle_registro(modelo, registro)
            else:
                identificador = input("ID del registro: ").strip()

                if identificador.isdigit():
                    registro = buscar_registro(
                        modelo, int(identificador)
                    )

                    if registro:
                        _mostrar_detalle_registro(modelo, registro)
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
                        # usa actualizar_usuario y maneja errores de RUT repetido/inválido
                        try:
                            if modelo is Usuario:
                                actualizar_usuario(int(identificador), datos)
                            else:
                                actualizar_registro(
                                    modelo,
                                    int(identificador),
                                    datos,
                                )
                        except (ValueError, IntegrityError) as err:
                            print(f"No se pudo actualizar: {err}")
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
                        "¿Eliminar? Escribe si para confirmar: "
                    )

                    if confirmar.strip().upper() == "SI":
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
