from peewee import IntegrityError
from auxiliares.hasheo import hash_password
from auxiliares.validaciones import (
    normalizar_rut,
    validar_email,
    validar_password,
    validar_rut,
)
from datos.modelos.models import Usuario
from datos.repositorio.usuarios import (
    actualizar_usuario as actualizar_usuario_repo,
    buscar_usuario as buscar_usuario_repo,
    buscar_usuario_por_rut as buscar_usuario_por_rut_repo,
    crear_usuario as crear_usuario_repo,
    eliminar_usuario as eliminar_usuario_repo,
    listar_usuarios as listar_usuarios_repo,
)


def crear_usuario(datos: dict):
    """Crea un usuario validando que el RUT sea válido y no esté repetido."""
    if not validar_email(datos.get("email", "")):
        raise ValueError("El correo debe tener un formato válido, por ejemplo nombre@dominio.cl.")
    if not validar_password(datos.get("password", "")):
        raise ValueError("La contraseña debe tener al menos 8 caracteres, una mayúscula, un número y un símbolo.")
    # valida el RUT ingresado antes de crear el registro
    rut_ingresado = datos.get("rut", "")
    if not validar_rut(rut_ingresado):
        raise ValueError("El RUT ingresado no es válido.")

    datos_limpios = dict(datos)
    datos_limpios["rut"] = normalizar_rut(rut_ingresado)  # normaliza el RUT
    datos_limpios["password"] = hash_password(datos_limpios["password"])

    # impide crear un segundo usuario con el mismo RUT
    if Usuario.select().where(Usuario.rut == datos_limpios["rut"]).exists():
        raise ValueError(f"El RUT {datos_limpios['rut']} ya está registrado en otro usuario.")

    try:
        return crear_usuario_repo(datos_limpios)
    except IntegrityError as exc:  # [CAMBIO RUT]: respaldo ante condición de carrera en BD
        raise ValueError(f"No se pudo crear el usuario: el RUT {datos_limpios['rut']} ya existe.") from exc


def listar_usuarios():
    return listar_usuarios_repo()


def buscar_usuario(identificador):
    return buscar_usuario_repo(identificador)


# función para buscar un usuario por su RUT 
def buscar_usuario_por_rut(rut: str):
    """Busca y retorna un objeto Usuario por su RUT (o None si no existe)."""
    if not validar_rut(rut):
        raise ValueError("El RUT ingresado para buscar no es válido.")

    rut_norm = normalizar_rut(rut)
    return buscar_usuario_por_rut_repo(rut_norm)


def actualizar_usuario(identificador, datos: dict):
    datos_limpios = dict(datos)

    if "email" in datos_limpios and not validar_email(datos_limpios["email"]):
        raise ValueError("El correo debe tener un formato válido, por ejemplo nombre@dominio.cl.")
    if "password" in datos_limpios and not validar_password(datos_limpios["password"]):
        raise ValueError("La contraseña debe tener al menos 8 caracteres, una mayúscula, un número y un símbolo.")

    if "password" in datos_limpios:
        datos_limpios["password"] = hash_password(datos_limpios["password"])

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

    return actualizar_usuario_repo(identificador, datos_limpios)


def eliminar_usuario(identificador):
    return eliminar_usuario_repo(identificador)
