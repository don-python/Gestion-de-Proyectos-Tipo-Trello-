from datos.modelos.models import Etiqueta
from datos.repositorio.operaciones import (
    crear_registro,
    listar_registros,
    buscar_registro,
    actualizar_registro,
    eliminar_registro,
)


def crear_etiqueta(datos):
    return crear_registro(Etiqueta, datos)


def listar_etiquetas():
    return listar_registros(Etiqueta)


def buscar_etiqueta(identificador):
    return buscar_registro(Etiqueta, identificador)


def actualizar_etiqueta(identificador, datos):
    return actualizar_registro(Etiqueta, identificador, datos)


def eliminar_etiqueta(identificador):
    return eliminar_registro(Etiqueta, identificador)
