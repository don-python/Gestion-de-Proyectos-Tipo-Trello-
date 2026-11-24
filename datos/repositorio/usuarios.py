from datos.modelos.models import Usuario
from datos.repositorio.operaciones import (
    actualizar_registro,
    buscar_registro,
    crear_registro,
    eliminar_registro,
    listar_registros,
)


def crear_usuario(datos):
    return crear_registro(Usuario, datos)


def listar_usuarios():
    return listar_registros(Usuario)


def buscar_usuario(identificador):
    return buscar_registro(Usuario, identificador)


def buscar_usuario_por_rut(rut):
    with Usuario._meta.database.connection_context():
        return Usuario.get_or_none(Usuario.rut == rut)


def actualizar_usuario(identificador, datos):
    return actualizar_registro(Usuario, identificador, datos)


def eliminar_usuario(identificador):
    return eliminar_registro(Usuario, identificador)
