from peewee import IntegrityError

from datos.modelos.models import ProyectoUsuario, TarjetaEtiqueta


def listar_participantes():
    with ProyectoUsuario._meta.database.connection_context():
        return list(ProyectoUsuario.select())


def agregar_participante(proyecto_id, usuario_id):
    try:
        with ProyectoUsuario._meta.database.connection_context():
            with ProyectoUsuario._meta.database.atomic():
                ProyectoUsuario.create(proyecto=proyecto_id, usuario=usuario_id)
        return True
    except IntegrityError:
        return False
    except Exception:
        return False


def eliminar_participante(proyecto_id, usuario_id):
    try:
        with ProyectoUsuario._meta.database.connection_context():
            cantidad = ProyectoUsuario.delete().where(
                (ProyectoUsuario.proyecto == proyecto_id)
                & (ProyectoUsuario.usuario == usuario_id)
            ).execute()
        return cantidad > 0
    except Exception:
        return False


def listar_asociaciones():
    with TarjetaEtiqueta._meta.database.connection_context():
        return list(TarjetaEtiqueta.select())


def asociar_etiqueta(tarjeta_id, etiqueta_id):
    try:
        with TarjetaEtiqueta._meta.database.connection_context():
            with TarjetaEtiqueta._meta.database.atomic():
                TarjetaEtiqueta.create(tarjeta=tarjeta_id, etiqueta=etiqueta_id)
        return True
    except IntegrityError:
        return False
    except Exception:
        return False


def desasociar_etiqueta(tarjeta_id, etiqueta_id):
    try:
        with TarjetaEtiqueta._meta.database.connection_context():
            cantidad = TarjetaEtiqueta.delete().where(
                (TarjetaEtiqueta.tarjeta == tarjeta_id)
                & (TarjetaEtiqueta.etiqueta == etiqueta_id)
            ).execute()
        return cantidad > 0
    except Exception:
        return False
