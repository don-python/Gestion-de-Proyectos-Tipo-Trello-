from peewee import IntegrityError, DoesNotExist, ForeignKeyField, CompositeKey
from prettytable import PrettyTable


def crear_registro(modelo, datos):
    """Crea un registro nuevo."""
    try:
        with modelo._meta.database.connection_context():
            with modelo._meta.database.atomic():
                registro = modelo.create(**datos)

        print("Registro creado correctamente.")
        return registro

    except IntegrityError:
        print("No se pudo crear: revisa las claves y restricciones.")
        return None

    except (TypeError, ValueError) as error:
        print(f"Datos inválidos: {error}")
        return None

    except Exception as error:
        print(f"Error al crear el registro: {error}")
        return None


def listar_registros(modelo):
    """Muestra los registros de una tabla."""
    try:
        with modelo._meta.database.connection_context():
            registros = list(modelo.select())

        if not registros:
            print("No hay registros para mostrar.")
            return []

        tabla = PrettyTable()
        campos = list(modelo._meta.fields.keys())
        tabla.field_names = campos

        for registro in registros:
            fila = []

            for campo in campos:
                valor = getattr(registro, campo)

                if isinstance(valor, modelo):
                    valor = valor.get_id()
                elif hasattr(valor, "get_id"):
                    valor = valor.get_id()

                fila.append(valor)

            tabla.add_row(fila)

        print(tabla)
        return registros

    except Exception as error:
        print(f"Error al listar los registros: {error}")
        return []


def buscar_registro(modelo, identificador):
    """Busca un registro por su ID individual."""
    if isinstance(modelo._meta.primary_key, CompositeKey):
        print("Este modelo necesita una búsqueda por clave compuesta.")
        return None

    try:
        with modelo._meta.database.connection_context():
            return modelo.get_by_id(identificador)

    except DoesNotExist:
        print("No se encontró el registro.")
        return None

    except (ValueError, TypeError) as error:
        print(f"Identificador inválido: {error}")
        return None

    except Exception as error:
        print(f"Error al buscar el registro: {error}")
        return None


def actualizar_registro(modelo, identificador, datos):
    """Actualiza los campos indicados de un registro."""
    if not datos:
        print("No se proporcionaron datos para actualizar.")
        return False

    if isinstance(modelo._meta.primary_key, CompositeKey):
        print("Este modelo necesita una actualización por clave compuesta.")
        return False

    campos = modelo._meta.fields

    # Validar todos los campos antes de modificar el registro.
    for campo in datos:
        nombre = campo[:-3] if campo.endswith("_id") else campo

        if nombre not in campos:
            print(f"El campo '{campo}' no existe.")
            return False

        if campos[nombre].primary_key:
            print("No se permite modificar la clave primaria.")
            return False

        if campo.endswith("_id") and not isinstance(
            campos[nombre], ForeignKeyField
        ):
            print(f"'{campo}' no es una clave foránea válida.")
            return False

    try:
        with modelo._meta.database.connection_context():
            with modelo._meta.database.atomic():
                registro = modelo.get_by_id(identificador)

                for campo, valor in datos.items():
                    nombre = campo[:-3] if campo.endswith("_id") else campo
                    setattr(registro, nombre, valor)

                registro.save()

        print("Registro actualizado correctamente.")
        return True

    except DoesNotExist:
        print("No se encontró el registro.")
        return False

    except IntegrityError:
        print("No se pudo actualizar: revisa las claves y restricciones.")
        return False

    except (ValueError, TypeError) as error:
        print(f"Datos inválidos: {error}")
        return False

    except Exception as error:
        print(f"Error al actualizar el registro: {error}")
        return False


def eliminar_registro(modelo, identificador):
    """Elimina un registro por su ID individual."""
    if isinstance(modelo._meta.primary_key, CompositeKey):
        print("Este modelo necesita una eliminación por clave compuesta.")
        return False

    try:
        with modelo._meta.database.connection_context():
            with modelo._meta.database.atomic():
                registro = modelo.get_by_id(identificador)
                registro.delete_instance()

        print("Registro eliminado correctamente.")
        return True

    except DoesNotExist:
        print("No se encontró el registro.")
        return False

    except IntegrityError:
        print("No se puede eliminar: existen registros relacionados.")
        return False

    except Exception as error:
        print(f"Error al eliminar el registro: {error}")
        return False
