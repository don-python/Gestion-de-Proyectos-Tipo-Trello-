from orm.models import Usuario
from crud.operaciones import (
    crear_registro,
    listar_registros,
    buscar_registro,
    actualizar_registro,
    eliminar_registro,
)


def crear_usuario(datos):
    return crear_registro(Usuario, datos)


def listar_usuarios():
    return listar_registros(Usuario)


def buscar_usuario(identificador):
    return buscar_registro(Usuario, identificador)


def actualizar_usuario(identificador, datos):
    return actualizar_registro(Usuario, identificador, datos)


def eliminar_usuario(identificador):
    return eliminar_registro(Usuario, identificador)
