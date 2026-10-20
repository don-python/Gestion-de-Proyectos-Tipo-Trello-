from orm.models import Proyecto
from crud.operaciones import (
    crear_registro,
    listar_registros,
    buscar_registro,
    actualizar_registro,
    eliminar_registro,
)


def crear_proyecto(datos):
    return crear_registro(Proyecto, datos)


def listar_proyectos():
    return listar_registros(Proyecto)


def buscar_proyecto(identificador):
    return buscar_registro(Proyecto, identificador)


def actualizar_proyecto(identificador, datos):
    return actualizar_registro(Proyecto, identificador, datos)


def eliminar_proyecto(identificador):
    return eliminar_registro(Proyecto, identificador)
