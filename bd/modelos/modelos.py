from peewee import *

# Conexión a MySQL (instalar antes: pip install peewee pymysql)
database = MySQLDatabase(
    'gestion_proyectos',
    charset='utf8mb4',
    host='localhost',
    user='root',
    password='',
)

ESTADOS_TARJETA = ('PENDIENTE', 'EN_PROGRESO', 'COMPLETADA', 'BLOQUEADA')


class BaseModel(Model):
    class Meta:
        database = database


class Proyecto(BaseModel):
    nombre = CharField(max_length=100)
    descripcion = CharField(max_length=255, null=True)
    fechaCreacion = DateField(column_name='fechaCreacion')

    class Meta:
        table_name = 'Proyecto'


class Tablero(BaseModel):
    nombre = CharField(max_length=100)
    proyecto = ForeignKeyField(Proyecto, column_name='proyecto_id', unique=True,
                               backref='tablero')

    class Meta:
        table_name = 'Tablero'


class Lista(BaseModel):
    nombre = CharField(max_length=100)
    posicion = IntegerField()
    tablero = ForeignKeyField(Tablero, column_name='tablero_id', backref='listas')

    class Meta:
        table_name = 'Lista'


class Usuario(BaseModel):
    nombre = CharField(max_length=100)
    email = CharField(max_length=150)

    class Meta:
        table_name = 'Usuario'


class Tarjeta(BaseModel):
    titulo = CharField(max_length=150)
    descripcion = CharField(max_length=500, null=True)
    fechaLimite = DateField(column_name='fechaLimite', null=True)
    estado = CharField(max_length=50, default='PENDIENTE')
    lista = ForeignKeyField(Lista, column_name='lista_id', backref='tarjetas')
    responsable = ForeignKeyField(Usuario, column_name='responsable_id', null=True,
                                  backref='tarjetas_asignadas')

    class Meta:
        table_name = 'Tarjeta'


class Etiqueta(BaseModel):
    nombre = CharField(max_length=100)
    color = CharField(max_length=50)

    class Meta:
        table_name = 'Etiqueta'


class Comentario(BaseModel):
    contenido = CharField(max_length=500)
    fechaCreacion = DateField(column_name='fechaCreacion')
    tarjeta = ForeignKeyField(Tarjeta, column_name='tarjeta_id', backref='comentarios')

    class Meta:
        table_name = 'Comentario'


class ProyectoUsuario(BaseModel):
    proyecto = ForeignKeyField(Proyecto, column_name='proyecto_id', backref='miembros')
    usuario = ForeignKeyField(Usuario, column_name='usuario_id', backref='proyectos')

    class Meta:
        table_name = 'Proyecto_Usuario'
        primary_key = CompositeKey('proyecto', 'usuario')


class TarjetaEtiqueta(BaseModel):
    tarjeta = ForeignKeyField(Tarjeta, column_name='tarjeta_id', backref='etiquetas')
    etiqueta = ForeignKeyField(Etiqueta, column_name='etiqueta_id', backref='tarjetas')

    class Meta:
        table_name = 'Tarjeta_Etiqueta'
        primary_key = CompositeKey('tarjeta', 'etiqueta')
