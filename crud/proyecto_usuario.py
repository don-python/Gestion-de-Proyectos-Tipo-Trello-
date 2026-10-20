
from peewee import IntegrityError
from orm.models import ProyectoUsuario


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
