
from peewee import IntegrityError
from orm.models import TarjetaEtiqueta


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
