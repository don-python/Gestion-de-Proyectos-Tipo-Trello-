from orm.models import Tarjeta
from crud.operaciones import (
    crear_registro,
    listar_registros,
    buscar_registro,
    actualizar_registro,
    eliminar_registro,
)


def crear_tarjeta(datos):
    return crear_registro(Tarjeta, datos)


def listar_tarjetas():
    return listar_registros(Tarjeta)


def buscar_tarjeta(identificador):
    return buscar_registro(Tarjeta, identificador)


def actualizar_tarjeta(identificador, datos):
    return actualizar_registro(Tarjeta, identificador, datos)


def eliminar_tarjeta(identificador):
    return eliminar_registro(Tarjeta, identificador)
