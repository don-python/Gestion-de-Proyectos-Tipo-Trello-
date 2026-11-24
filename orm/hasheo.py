import base64
import hashlib
import re

import bcrypt


def _bcrypt_input(password: str) -> bytes:
    """Pre-hash to support passwords longer than BCrypt's 72-byte limit."""
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)


def hash_password(password: str) -> str:
    """Devuelve un hash BCrypt con una sal aleatoria."""
    return bcrypt.hashpw(_bcrypt_input(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Compara una contraseña en texto con un hash BCrypt almacenado."""
    try:
        return bcrypt.checkpw(
            _bcrypt_input(plain_password),
            stored_hash.encode("utf-8"),
        )
    except (AttributeError, TypeError, ValueError):
        return False


def is_bcrypt_hash(stored_hash: str) -> bool:
    return isinstance(stored_hash, str) and stored_hash.startswith(("$2a$", "$2b$", "$2y$"))


def is_legacy_pbkdf2_hash(stored_hash: str) -> bool:
    """Reconoce el formato anterior para conservar cuentas hasta su cambio de clave."""
    return isinstance(stored_hash, str) and re.fullmatch(r"[0-9a-fA-F]{32}\$[0-9a-fA-F]{64}", stored_hash) is not None
