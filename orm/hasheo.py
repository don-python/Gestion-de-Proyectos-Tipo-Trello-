import hashlib 
import os

def hash_password(password: str) -> str:
    """hashear una contraseña"""

    salt = os.urandom(16)
    #aplicar la funcion hash
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    #retornar valores unidos por $
    return salt.hex() + '$' + pwd_hash.hex()

def verify_password(plain_password: str, stored_hash: str) -> bool:
    """
    Verifica si una contraseña escrita coincide con el hash guardado en la BD.
    """
    try:
        # Separa la sal y el hash guardados
        salt_hex, pwd_hex = stored_hash.split('$')
        salt = bytes.fromhex(salt_hex)
        stored_pwd_bytes = bytes.fromhex(pwd_hex)
        
        # Vuelve a hashear la contraseña ingresada con la misma sal
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256', 
            plain_password.encode('utf-8'), 
            salt, 
            100000
        )
        
        # Compara de forma segura ambos hashes
        return pwd_hash == stored_pwd_bytes
    except Exception:
        return False