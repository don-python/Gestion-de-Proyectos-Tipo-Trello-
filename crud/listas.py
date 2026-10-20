from orm.models import Lista
from crud.operaciones import (
    crear_registro,
    listar_registros,
    buscar_registro,
    actualizar_registro,
    eliminar_registro,
)


def crear_lista(datos):
    return crear_registro(Lista, datos)


def listar_listas():
    return listar_registros(Lista)


def buscar_lista(identificador):
    return buscar_registro(Lista, identificador)


def actualizar_lista(identificador, datos):
    return actualizar_registro(Lista, identificador, datos)


def eliminar_lista(identificador):
    return eliminar_registro(Lista, identificador)
