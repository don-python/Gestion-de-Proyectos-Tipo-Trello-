from peewee import IntegrityError  
from orm.models import Usuario, normalizar_rut, validar_rut  
from crud.operaciones import (
    crear_registro,
    listar_registros,
    buscar_registro,
    actualizar_registro,
    eliminar_registro,
)


def crear_usuario(datos: dict):
    """Crea un usuario validando que el RUT sea válido y no esté repetido."""
    # valida el RUT ingresado antes de crear el registro
    rut_ingresado = datos.get("rut", "")
    if not validar_rut(rut_ingresado):
        raise ValueError("El RUT ingresado no es válido.")

    datos_limpios = dict(datos)
    datos_limpios["rut"] = normalizar_rut(rut_ingresado)  # normaliza el RUT

    # impide crear un segundo usuario con el mismo RUT
    if Usuario.select().where(Usuario.rut == datos_limpios["rut"]).exists():
        raise ValueError(f"El RUT {datos_limpios['rut']} ya está registrado en otro usuario.")

    try:
        return crear_registro(Usuario, datos_limpios)
    except IntegrityError as exc:  # [CAMBIO RUT]: respaldo ante condición de carrera en BD
        raise ValueError(f"No se pudo crear el usuario: el RUT {datos_limpios['rut']} ya existe.") from exc


def listar_usuarios():
    return listar_registros(Usuario)


def buscar_usuario(identificador):
    return buscar_registro(Usuario, identificador)


# función para buscar un usuario por su RUT 
def buscar_usuario_por_rut(rut: str):
    """Busca y retorna un objeto Usuario por su RUT (o None si no existe)."""
    if not validar_rut(rut):
        raise ValueError("El RUT ingresado para buscar no es válido.")

    rut_norm = normalizar_rut(rut)
    return Usuario.get_or_none(Usuario.rut == rut_norm)


def actualizar_usuario(identificador, datos: dict):
    datos_limpios = dict(datos)

    # valida y evita duplicados al actualizar el RUT de un usuario
    if "rut" in datos_limpios and datos_limpios["rut"] is not None:
        if not validar_rut(datos_limpios["rut"]):
            raise ValueError("El nuevo RUT ingresado no es válido.")

        rut_norm = normalizar_rut(datos_limpios["rut"])
        duplicado = (
            Usuario.select()
            .where((Usuario.rut == rut_norm) & (Usuario.id != identificador))
            .exists()
        )
        if duplicado:
            raise ValueError(f"El RUT {rut_norm} ya pertenece a otro usuario.")

        datos_limpios["rut"] = rut_norm

    return actualizar_registro(Usuario, identificador, datos_limpios)


def eliminar_usuario(identificador):
    return eliminar_registro(Usuario, identificador)