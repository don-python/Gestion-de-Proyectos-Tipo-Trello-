from orm.models import Tablero
from crud.operaciones import (
    crear_registro,
    listar_registros,
    buscar_registro,
    actualizar_registro,
    eliminar_registro,
)


def crear_tablero(datos):
    return crear_registro(Tablero, datos)


def listar_tableros():
    return listar_registros(Tablero)


def buscar_tablero(identificador):
    return buscar_registro(Tablero, identificador)


def actualizar_tablero(identificador, datos):
    return actualizar_registro(Tablero, identificador, datos)


def eliminar_tablero(identificador):
    return eliminar_registro(Tablero, identificador)
