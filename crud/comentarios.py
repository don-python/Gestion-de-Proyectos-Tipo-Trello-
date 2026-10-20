from orm.models import Comentario
from crud.operaciones import (
    crear_registro,
    listar_registros,
    buscar_registro,
    actualizar_registro,
    eliminar_registro,
)


def crear_comentario(datos):
    return crear_registro(Comentario, datos)


def listar_comentarios():
    return listar_registros(Comentario)


def buscar_comentario(identificador):
    return buscar_registro(Comentario, identificador)


def actualizar_comentario(identificador, datos):
    return actualizar_registro(Comentario, identificador, datos)


def eliminar_comentario(identificador):
    return eliminar_registro(Comentario, identificador)
