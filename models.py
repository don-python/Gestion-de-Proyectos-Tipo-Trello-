from peewee import *#NOSONAR

# Configura tu conexión a MySQL
database = MySQLDatabase('gestion_proyectos', **{'charset': 'utf8mb4', 'host': 'localhost', 'user': 'root', 'password': ''})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Proyecto(BaseModel):
    descripcion = CharField(max_length=255, null=True)
    fechaCreacion = DateField(column_name='fechaCreacion')
    nombre = CharField(max_length=100)

    class Meta:
        table_name = 'proyecto'

class Tablero(BaseModel):
    nombre = CharField(max_length=100)
    proyecto = ForeignKeyField(column_name='proyecto_id', model=Proyecto, unique=True, field='id')

    class Meta:
        table_name = 'tablero'

class Lista(BaseModel):
    nombre = CharField(max_length=100)
    posicion = IntegerField()
    tablero = ForeignKeyField(column_name='tablero_id', model=Tablero, field='id')

    class Meta:
        table_name = 'lista'

class Usuario(BaseModel):
    email = CharField(max_length=150)
    nombre = CharField(max_length=100)

    class Meta:
        table_name = 'usuario'

class Tarjeta(BaseModel):
    descripcion = CharField(max_length=500, null=True)
    estado = CharField(max_length=50, default='PENDIENTE')
    fechaLimite = DateField(column_name='fechaLimite', null=True)
    lista = ForeignKeyField(column_name='lista_id', model=Lista, field='id')
    responsable = ForeignKeyField(column_name='responsable_id', model=Usuario, null=True, field='id')
    titulo = CharField(max_length=150)

    class Meta:
        table_name = 'tarjeta'

class Etiqueta(BaseModel):
    color = CharField(max_length=50)
    nombre = CharField(max_length=100)

    class Meta:
        table_name = 'etiqueta'

class Comentario(BaseModel):
    contenido = CharField(max_length=500)
    fechaCreacion = DateField(column_name='fechaCreacion')
    tarjeta = ForeignKeyField(column_name='tarjeta_id', model=Tarjeta, field='id')

    class Meta:
        table_name = 'comentario'

class ProyectoUsuario(BaseModel):
    proyecto = ForeignKeyField(column_name='proyecto_id', model=Proyecto, field='id')
    usuario = ForeignKeyField(column_name='usuario_id', model=Usuario, field='id')

    class Meta:
        table_name = 'proyecto_usuario'
        primary_key = CompositeKey('proyecto', 'usuario')

class TarjetaEtiqueta(BaseModel):
    etiqueta = ForeignKeyField(column_name='etiqueta_id', model=Etiqueta, field='id')
    tarjeta = ForeignKeyField(column_name='tarjeta_id', model=Tarjeta, field='id')

    class Meta:
        table_name = 'tarjeta_etiqueta'
        primary_key = CompositeKey('etiqueta', 'tarjeta')

