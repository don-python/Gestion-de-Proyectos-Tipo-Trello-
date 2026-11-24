import re


def normalizar_rut(rut: str) -> str:
    """Limpia puntos y espacios, y devuelve el RUT como cuerpo-dígito."""
    if not isinstance(rut, str):
        raise ValueError("El RUT debe ser un texto.")
    limpio = re.sub(r"[^0-9kK]", "", rut).upper()
    if len(limpio) < 2:
        raise ValueError("El RUT ingresado es demasiado corto.")
    cuerpo, dv = limpio[:-1], limpio[-1]
    if not cuerpo.isdigit():
        raise ValueError("El cuerpo del RUT solo debe contener dígitos.")
    return f"{int(cuerpo)}-{dv}"


def validar_rut(rut: str) -> bool:
    try:
        rut_norm = normalizar_rut(rut)
    except ValueError:
        return False

    cuerpo, dv = rut_norm.split("-")
    suma = 0
    multiplicador = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    resto = 11 - (suma % 11)
    esperado = "0" if resto == 11 else "K" if resto == 10 else str(resto)
    return dv == esperado


def validar_email(email: str) -> bool:
    if not isinstance(email, str):
        return False
    patron = (
        r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
        r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
        r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)*"
        r"\.[A-Za-z]{2,}"
    )
    return re.fullmatch(patron, email.strip()) is not None


def validar_password(password: str) -> bool:
    return (
        isinstance(password, str)
        and len(password) >= 8
        and any(caracter.isupper() for caracter in password)
        and any(caracter.isdigit() for caracter in password)
        and any(not caracter.isalnum() and not caracter.isspace() for caracter in password)
    )
