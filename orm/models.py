import os
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
    def __init__(self, *_, **__): pass

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

class Usuario(BaseModel):
    email = CharField(max_length=150)
    nombre = CharField(max_length=100)

    class Meta:
        table_name = 'usuario'

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

