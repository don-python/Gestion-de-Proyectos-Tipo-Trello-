from datetime import date

from peewee import IntegrityError

from modelos import (
    database, ESTADOS_TARJETA,
    Proyecto, Tablero, Lista, Usuario, Tarjeta, Etiqueta,
    Comentario, ProyectoUsuario, TarjetaEtiqueta,
)



# Helpers genéricos
def _actualizar(modelo, id_, **campos):
    """Actualiza solo los campos que no son None. Devuelve filas afectadas."""
    campos = {k: v for k, v in campos.items() if v is not None}
    if not campos:
        return 0
    return modelo.update(**campos).where(modelo.id == id_).execute()


def _eliminar(modelo, id_):
    """Elimina un registro y todo lo que depende de él (hijos primero)."""
    obj = modelo.get_or_none(modelo.id == id_)
    if obj is None:
        return False
    obj.delete_instance(recursive=True)
    return True



# PROYECTO
def crear_proyecto(nombre, descripcion=None):
    return Proyecto.create(nombre=nombre, descripcion=descripcion,
                           fechaCreacion=date.today())

def obtener_proyecto(id_):
    return Proyecto.get_or_none(Proyecto.id == id_)

def listar_proyectos():
    return list(Proyecto.select().order_by(Proyecto.id))

def actualizar_proyecto(id_, nombre=None, descripcion=None):
    return _actualizar(Proyecto, id_, nombre=nombre, descripcion=descripcion)

def eliminar_proyecto(id_):
    return _eliminar(Proyecto, id_)


# TABLERO (1 por proyecto)

def crear_tablero(nombre, proyecto_id):
    try:
        return Tablero.create(nombre=nombre, proyecto=proyecto_id)
    except IntegrityError:
        print(f"El proyecto {proyecto_id} no existe o ya tiene un tablero.")
        return None

def obtener_tablero(id_):
    return Tablero.get_or_none(Tablero.id == id_)

def obtener_tablero_de_proyecto(proyecto_id):
    return Tablero.get_or_none(Tablero.proyecto == proyecto_id)

def listar_tableros():
    return list(Tablero.select())

def actualizar_tablero(id_, nombre=None):
    return _actualizar(Tablero, id_, nombre=nombre)

def eliminar_tablero(id_):
    return _eliminar(Tablero, id_)



# LISTA
def crear_lista(nombre, tablero_id, posicion=None):
    if posicion is None:  # la deja al final
        posicion = Lista.select().where(Lista.tablero == tablero_id).count() + 1
    try:
        return Lista.create(nombre=nombre, posicion=posicion, tablero=tablero_id)
    except IntegrityError:
        print(f"El tablero {tablero_id} no existe.")
        return None

def obtener_lista(id_):
    return Lista.get_or_none(Lista.id == id_)

def listar_listas(tablero_id):
    return list(Lista.select().where(Lista.tablero == tablero_id)
                .order_by(Lista.posicion))

def actualizar_lista(id_, nombre=None, posicion=None):
    return _actualizar(Lista, id_, nombre=nombre, posicion=posicion)

def eliminar_lista(id_):
    return _eliminar(Lista, id_)



# USUARIO
def crear_usuario(nombre, email):
    if Usuario.select().where(Usuario.email == email).exists():
        print(f"Ya existe un usuario con el email {email}.")
        return None
    return Usuario.create(nombre=nombre, email=email)

def obtener_usuario(id_):
    return Usuario.get_or_none(Usuario.id == id_)

def listar_usuarios():
    return list(Usuario.select())

def actualizar_usuario(id_, nombre=None, email=None):
    return _actualizar(Usuario, id_, nombre=nombre, email=email)

def eliminar_usuario(id_):
    # Las tarjetas que tenía asignadas quedan con responsable NULL
    with database.atomic():
        Tarjeta.update(responsable=None).where(Tarjeta.responsable == id_).execute()
        return _eliminar(Usuario, id_)



# TARJETA
def crear_tarjeta(titulo, lista_id, descripcion=None, fecha_limite=None,
                  responsable_id=None, estado='PENDIENTE'):
    if estado not in ESTADOS_TARJETA:
        raise ValueError(f"Estado inválido. Usa uno de: {ESTADOS_TARJETA}")
    try:
        return Tarjeta.create(titulo=titulo, descripcion=descripcion,
                              fechaLimite=fecha_limite, estado=estado,
                              lista=lista_id, responsable=responsable_id)
    except IntegrityError:
        print("La lista o el responsable indicado no existe.")
        return None

def obtener_tarjeta(id_):
    return Tarjeta.get_or_none(Tarjeta.id == id_)

def listar_tarjetas(lista_id=None, estado=None):
    q = Tarjeta.select()
    if lista_id is not None:
        q = q.where(Tarjeta.lista == lista_id)
    if estado is not None:
        q = q.where(Tarjeta.estado == estado)
    return list(q)

def actualizar_tarjeta(id_, titulo=None, descripcion=None, fecha_limite=None):
    return _actualizar(Tarjeta, id_, titulo=titulo, descripcion=descripcion,
                       fechaLimite=fecha_limite)

def cambiar_estado_tarjeta(id_, estado):
    if estado not in ESTADOS_TARJETA:
        raise ValueError(f"Estado inválido. Usa uno de: {ESTADOS_TARJETA}")
    return _actualizar(Tarjeta, id_, estado=estado)

def mover_tarjeta(id_, nueva_lista_id):
    return _actualizar(Tarjeta, id_, lista=nueva_lista_id)

def asignar_responsable(id_, usuario_id):
    return _actualizar(Tarjeta, id_, responsable=usuario_id)

def quitar_responsable(id_):
    return Tarjeta.update(responsable=None).where(Tarjeta.id == id_).execute()

def eliminar_tarjeta(id_):
    return _eliminar(Tarjeta, id_)



# ETIQUETA
def crear_etiqueta(nombre, color):
    return Etiqueta.create(nombre=nombre, color=color)

def obtener_etiqueta(id_):
    return Etiqueta.get_or_none(Etiqueta.id == id_)

def listar_etiquetas():
    return list(Etiqueta.select())

def actualizar_etiqueta(id_, nombre=None, color=None):
    return _actualizar(Etiqueta, id_, nombre=nombre, color=color)

def eliminar_etiqueta(id_):
    return _eliminar(Etiqueta, id_)



# COMENTARIO
def crear_comentario(contenido, tarjeta_id):
    try:
        return Comentario.create(contenido=contenido, tarjeta=tarjeta_id,
                                 fechaCreacion=date.today())
    except IntegrityError:
        print(f"La tarjeta {tarjeta_id} no existe.")
        return None

def listar_comentarios(tarjeta_id):
    return list(Comentario.select().where(Comentario.tarjeta == tarjeta_id))

def actualizar_comentario(id_, contenido):
    return _actualizar(Comentario, id_, contenido=contenido)

def eliminar_comentario(id_):
    return _eliminar(Comentario, id_)



# RELACIONES N:M  (Proyecto_Usuario y Tarjeta_Etiqueta)
# Estas tablas no tienen "id", se manejan con delete().where()
def agregar_usuario_a_proyecto(proyecto_id, usuario_id):
    try:
        ProyectoUsuario.create(proyecto=proyecto_id, usuario=usuario_id)
        return True
    except IntegrityError:
        print("Ya es miembro, o el proyecto/usuario no existe.")
        return False

def quitar_usuario_de_proyecto(proyecto_id, usuario_id):
    return ProyectoUsuario.delete().where(
        (ProyectoUsuario.proyecto == proyecto_id) &
        (ProyectoUsuario.usuario == usuario_id)
    ).execute()

def listar_miembros(proyecto_id):
    return list(Usuario.select().join(ProyectoUsuario)
                .where(ProyectoUsuario.proyecto == proyecto_id))

def agregar_etiqueta_a_tarjeta(tarjeta_id, etiqueta_id):
    try:
        TarjetaEtiqueta.create(tarjeta=tarjeta_id, etiqueta=etiqueta_id)
        return True
    except IntegrityError:
        print("La tarjeta ya tiene esa etiqueta, o alguna no existe.")
        return False

def quitar_etiqueta_de_tarjeta(tarjeta_id, etiqueta_id):
    return TarjetaEtiqueta.delete().where(
        (TarjetaEtiqueta.tarjeta == tarjeta_id) &
        (TarjetaEtiqueta.etiqueta == etiqueta_id)
    ).execute()

def listar_etiquetas_de_tarjeta(tarjeta_id):
    return list(Etiqueta.select().join(TarjetaEtiqueta)
                .where(TarjetaEtiqueta.tarjeta == tarjeta_id))


# Prueba rápida
if __name__ == "__main__":
    with database.connection_context():
        proyecto = crear_proyecto("App Trello", "Proyecto de prueba")
        tablero = crear_tablero("Sprint 1", proyecto.id)
        l1 = crear_lista("Por hacer", tablero.id)
        l2 = crear_lista("Hecho", tablero.id)

        ana = crear_usuario("Ana", "ana@mail.com")
        agregar_usuario_a_proyecto(proyecto.id, ana.id)

        t = crear_tarjeta("Diseñar login", l1.id, "Pantalla de acceso",
                          date(2026, 11, 1), responsable_id=ana.id)
        bug = crear_etiqueta("Bug", "#ff0000")
        agregar_etiqueta_a_tarjeta(t.id, bug.id)
        crear_comentario("Empezando hoy", t.id)

        cambiar_estado_tarjeta(t.id, "EN_PROGRESO")
        mover_tarjeta(t.id, l2.id)

        for tj in listar_tarjetas(lista_id=l2.id):
            print(tj.id, tj.titulo, tj.estado, tj.responsable.nombre)
        print("Etiquetas:", [e.nombre for e in listar_etiquetas_de_tarjeta(t.id)])
        print("Miembros:", [u.nombre for u in listar_miembros(proyecto.id)])

        eliminar_proyecto(proyecto.id)  # borra en cascada tablero, listas, tarjetas...
        eliminar_usuario(ana.id)
        eliminar_etiqueta(bug.id)
