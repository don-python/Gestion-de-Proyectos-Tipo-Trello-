import os
import re 
import hashlib
from dotenv import load_dotenv
from peewee import *

load_dotenv()

database = MySQLDatabase(
    os.getenv("DB_NAME"),
    charset="utf8mb4",
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = database


class Proyecto(BaseModel):
    descripcion = CharField(null=True)
    fecha_creacion = DateField(column_name='fechaCreacion')
    nombre = CharField(max_length=100)

    class Meta:
        table_name = 'proyecto'


class Tablero(BaseModel):
    nombre = CharField(max_length=100)
    proyecto = ForeignKeyField(column_name='proyecto_id', field='id', model=Proyecto, unique=True)

    class Meta:
        table_name = 'tablero'


class Lista(BaseModel):
    nombre = CharField(max_length=100)
    posicion = IntegerField()
    tablero = ForeignKeyField(column_name='tablero_id', field='id', model=Tablero)

    class Meta:
        table_name = 'lista'



# funciona para limpiar el RUT y validar su digito verificador
def normalizar_rut(rut: str) -> str:
    """Limpia puntos/espacios y devuelve el RUT en formato 'cuerpo-dv' en mayúsculas."""
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
    """Valida formato y dígito verificador mediante algoritmo módulo 11."""
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
    if resto == 11:
        dv_esperado = "0"
    elif resto == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(resto)

    return dv == dv_esperado


def validar_email(email: str) -> bool:
    """Valida una estructura básica usuario@dominio.ext."""
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
    """Exige 8 caracteres, mayúscula, número y símbolo no espaciador."""
    return (
        isinstance(password, str)
        and len(password) >= 8
        and any(caracter.isupper() for caracter in password)
        and any(caracter.isdigit() for caracter in password)
        and any(not caracter.isalnum() and not caracter.isspace() for caracter in password)
    )


# Integración de función de hasheo
def hash_password(password: str) -> str:
    """Hasheo de la contraseña"""
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return salt.hex() + '$' + pwd_hash.hex()


class Usuario(BaseModel):
    rut = CharField(max_length=12, unique=True)
    email = CharField(max_length=150)
    nombre = CharField(max_length=100)
    password = CharField(max_length=255)

    class Meta:
        table_name = 'usuario'

    def save(self, *args, **kwargs):
        """
        Valida y normaliza el RUT antes de guardar, y hashea la contraseña """
        #valida que el RUT tenga dígito verificador correcto antes de guardar
        if not validar_rut(self.rut):
            raise ValueError(f"RUT inválido: '{self.rut}'")
        
        #normaliza el RUT y verifica que no exista en otro usuario
        rut_formateado = normalizar_rut(self.rut)

        query = Usuario.select().where(Usuario.rut == rut_formateado)
        if self.id is not None:
            query = query.where(Usuario.id != self.id)
        if query.exists():
            raise ValueError(f"Ya existe un usuario registrado con el RUT {rut_formateado}.")
        #guarda el RUT en formato canónico sin puntos ni espacio y con digito verificador en mayuscula 
        self.rut = rut_formateado 

        if self.password and '$' not in self.password:
            if not validar_password(self.password):
                raise ValueError(
                    "La contraseña debe tener al menos 8 caracteres, una mayúscula, "
                    "un número y un símbolo."
                )
            self.password = hash_password(self.password)

        super().save(*args, **kwargs)


class Tarjeta(BaseModel):
    descripcion = CharField(max_length=500, null=True)
    estado = CharField(constraints=[SQL("DEFAULT 'PENDIENTE'")])
    fecha_limite = DateField(column_name='fechaLimite', null=True)
    lista = ForeignKeyField(column_name='lista_id', field='id', model=Lista)
    responsable = ForeignKeyField(column_name='responsable_id', field='id', model=Usuario, null=True)
    titulo = CharField(max_length=150)

    class Meta:
        table_name = 'tarjeta'


class Comentario(BaseModel):
    contenido = CharField(max_length=500)
    fecha_creacion = DateField(column_name='fechaCreacion')
    tarjeta = ForeignKeyField(column_name='tarjeta_id', field='id', model=Tarjeta)

    class Meta:
        table_name = 'comentario'


class Etiqueta(BaseModel):
    color = CharField(max_length=50)
    nombre = CharField(max_length=100)

    class Meta:
        table_name = 'etiqueta'


class ProyectoUsuario(BaseModel):
    proyecto = ForeignKeyField(column_name='proyecto_id', field='id', model=Proyecto)
    usuario = ForeignKeyField(column_name='usuario_id', field='id', model=Usuario)

    class Meta:
        table_name = 'proyecto_usuario'
        indexes = (
            (('proyecto', 'usuario'), True),
        )
        primary_key = CompositeKey('proyecto', 'usuario')


class TarjetaEtiqueta(BaseModel):
    etiqueta = ForeignKeyField(column_name='etiqueta_id', field='id', model=Etiqueta)
    tarjeta = ForeignKeyField(column_name='tarjeta_id', field='id', model=Tarjeta)

    class Meta:
        table_name = 'tarjeta_etiqueta'
        indexes = (
            (('tarjeta', 'etiqueta'), True),
        )
        primary_key = CompositeKey('tarjeta', 'etiqueta')
