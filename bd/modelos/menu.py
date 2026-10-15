from datetime import datetime

import crud
from modelos import (
    database, ESTADOS_TARJETA,
    Proyecto, Tablero, Lista, Usuario, Tarjeta, Etiqueta,
    Comentario, ProyectoUsuario, TarjetaEtiqueta,
)



# Helpers de entrada
def pedir_texto(msg, obligatorio=True):
    """Si no es obligatorio y se deja vacío, devuelve None (= no cambiar)."""
    while True:
        valor = input(msg).strip()
        if valor:
            return valor
        if not obligatorio:
            return None
        print("  Este campo es obligatorio.")


def pedir_int(msg, obligatorio=True):
    while True:
        valor = input(msg).strip()
        if not valor and not obligatorio:
            return None
        if valor.isdigit():
            return int(valor)
        print("  Ingresa un número válido.")


def pedir_fecha(msg):
    """Formato AAAA-MM-DD. Vacío = None."""
    while True:
        valor = input(msg).strip()
        if not valor:
            return None
        try:
            return datetime.strptime(valor, "%Y-%m-%d").date()
        except ValueError:
            print("  Formato inválido. Usa AAAA-MM-DD (ej: 2026-12-31).")


def confirmar(msg):
    return input(f"{msg} (s/n): ").strip().lower() == "s"


def pedir_estado():
    for i, e in enumerate(ESTADOS_TARJETA, 1):
        print(f"  {i}. {e}")
    while True:
        n = pedir_int("Estado: ")
        if 1 <= n <= len(ESTADOS_TARJETA):
            return ESTADOS_TARJETA[n - 1]
        print("  Opción fuera de rango.")


def ejecutar_menu(titulo, opciones, salida="Volver"):
    """opciones = [(texto, funcion), ...]"""
    while True:
        print(f"\n===== {titulo} =====")
        for i, (texto, _) in enumerate(opciones, 1):
            print(f"{i}. {texto}")
        print(f"0. {salida}")
        op = input("Opción: ").strip()
        if op == "0":
            return
        if op.isdigit() and 1 <= int(op) <= len(opciones):
            try:
                opciones[int(op) - 1][1]()
            except Exception as e:  # que un error no cierre el programa
                print(f"  Error: {e}")
        else:
            print("  Opción inválida.")



# Funciones para mostrar registros

def _mostrar(titulo, items, formato):
    print(f"\n--- {titulo} ---")
    if not items:
        print("  (sin registros)")
    for it in items:
        print("  " + formato(it))
    return items


def mostrar_proyectos():
    return _mostrar("Proyectos", crud.listar_proyectos(),
                    lambda p: f"[{p.id}] {p.nombre} | {p.descripcion or '-'} | creado: {p.fechaCreacion}")


def mostrar_tableros():
    return _mostrar("Tableros", crud.listar_tableros(),
                    lambda t: f"[{t.id}] {t.nombre} | proyecto: {t.proyecto.nombre}")


def mostrar_listas(tablero_id):
    return _mostrar("Listas", crud.listar_listas(tablero_id),
                    lambda l: f"[{l.id}] pos {l.posicion} - {l.nombre}")


def mostrar_usuarios():
    return _mostrar("Usuarios", crud.listar_usuarios(),
                    lambda u: f"[{u.id}] {u.nombre} <{u.email}>")


def mostrar_etiquetas():
    return _mostrar("Etiquetas", crud.listar_etiquetas(),
                    lambda e: f"[{e.id}] {e.nombre} ({e.color})")


def _fmt_tarjeta(t):
    resp = t.responsable.nombre if t.responsable else "-"
    return (f"[{t.id}] {t.titulo} | {t.estado} | lista: {t.lista.nombre} "
            f"| resp: {resp} | límite: {t.fechaLimite or '-'}")


def mostrar_tarjetas(lista_id=None, estado=None):
    return _mostrar("Tarjetas", crud.listar_tarjetas(lista_id, estado), _fmt_tarjeta)


def mostrar_todas_las_tablas():
    tablas = [Proyecto, Tablero, Lista, Usuario, Tarjeta, Etiqueta,
              Comentario, ProyectoUsuario, TarjetaEtiqueta]
    for modelo in tablas:
        print(f"\n=== {modelo._meta.table_name} ===")
        filas = list(modelo.select().dicts())
        if not filas:
            print("  (vacía)")
        for fila in filas:
            print(" ", fila)


def _eliminar_generico(nombre, obtener, eliminar, aviso=""):
    id_ = pedir_int(f"ID de {nombre} a eliminar: ")
    if obtener(id_) is None:
        print(f"  No existe {nombre} con id {id_}.")
        return
    if confirmar(f"¿Eliminar {nombre} {id_}? {aviso}"):
        eliminar(id_)
        print("  Eliminado.")
    else:
        print("  Cancelado.")



# PROYECTOS

def proyecto_crear():
    p = crud.crear_proyecto(pedir_texto("Nombre: "),
                            pedir_texto("Descripción (opcional): ", False))
    print(f"  Proyecto creado con id {p.id}.")


def proyecto_actualizar():
    mostrar_proyectos()
    id_ = pedir_int("ID del proyecto: ")
    if crud.obtener_proyecto(id_) is None:
        print("  No existe.")
        return
    print("  (deja vacío lo que no quieras cambiar)")
    crud.actualizar_proyecto(id_, pedir_texto("Nuevo nombre: ", False),
                             pedir_texto("Nueva descripción: ", False))
    print("  Actualizado.")


def proyecto_eliminar():
    mostrar_proyectos()
    _eliminar_generico("proyecto", crud.obtener_proyecto, crud.eliminar_proyecto,
                       "Se borrarán su tablero, listas, tarjetas y comentarios.")


def menu_proyectos():
    ejecutar_menu("PROYECTOS", [
        ("Crear proyecto", proyecto_crear),
        ("Listar proyectos", mostrar_proyectos),
        ("Actualizar proyecto", proyecto_actualizar),
        ("Eliminar proyecto", proyecto_eliminar),
    ])



# TABLEROS
def tablero_crear():
    mostrar_proyectos()
    pid = pedir_int("ID del proyecto: ")
    t = crud.crear_tablero(pedir_texto("Nombre del tablero: "), pid)
    if t:
        print(f"  Tablero creado con id {t.id}.")


def tablero_actualizar():
    mostrar_tableros()
    id_ = pedir_int("ID del tablero: ")
    if crud.obtener_tablero(id_) is None:
        print("  No existe.")
        return
    crud.actualizar_tablero(id_, pedir_texto("Nuevo nombre: ", False))
    print("  Actualizado.")


def tablero_eliminar():
    mostrar_tableros()
    _eliminar_generico("tablero", crud.obtener_tablero, crud.eliminar_tablero,
                       "Se borrarán sus listas y tarjetas.")


def menu_tableros():
    ejecutar_menu("TABLEROS", [
        ("Crear tablero", tablero_crear),
        ("Listar tableros", mostrar_tableros),
        ("Actualizar tablero", tablero_actualizar),
        ("Eliminar tablero", tablero_eliminar),
    ])



# LISTAS
def lista_crear():
    mostrar_tableros()
    tid = pedir_int("ID del tablero: ")
    pos = pedir_int("Posición (vacío = al final): ", False)
    l = crud.crear_lista(pedir_texto("Nombre de la lista: "), tid, pos)
    if l:
        print(f"  Lista creada con id {l.id}.")


def lista_listar():
    mostrar_tableros()
    mostrar_listas(pedir_int("ID del tablero: "))


def lista_actualizar():
    mostrar_tableros()
    mostrar_listas(pedir_int("ID del tablero: "))
    id_ = pedir_int("ID de la lista a editar: ")
    if crud.obtener_lista(id_) is None:
        print("  No existe.")
        return
    print("  (deja vacío lo que no quieras cambiar)")
    crud.actualizar_lista(id_, pedir_texto("Nuevo nombre: ", False),
                          pedir_int("Nueva posición: ", False))
    print("  Actualizada.")


def lista_eliminar():
    mostrar_tableros()
    mostrar_listas(pedir_int("ID del tablero: "))
    _eliminar_generico("lista", crud.obtener_lista, crud.eliminar_lista,
                       "Se borrarán sus tarjetas.")


def menu_listas():
    ejecutar_menu("LISTAS", [
        ("Crear lista", lista_crear),
        ("Listar listas de un tablero", lista_listar),
        ("Actualizar lista", lista_actualizar),
        ("Eliminar lista", lista_eliminar),
    ])



# USUARIOS
def usuario_crear():
    u = crud.crear_usuario(pedir_texto("Nombre: "), pedir_texto("Email: "))
    if u:
        print(f"  Usuario creado con id {u.id}.")


def usuario_actualizar():
    mostrar_usuarios()
    id_ = pedir_int("ID del usuario: ")
    if crud.obtener_usuario(id_) is None:
        print("  No existe.")
        return
    print("  (deja vacío lo que no quieras cambiar)")
    crud.actualizar_usuario(id_, pedir_texto("Nuevo nombre: ", False),
                            pedir_texto("Nuevo email: ", False))
    print("  Actualizado.")


def usuario_eliminar():
    mostrar_usuarios()
    _eliminar_generico("usuario", crud.obtener_usuario, crud.eliminar_usuario,
                       "Sus tarjetas quedarán sin responsable.")


def menu_usuarios():
    ejecutar_menu("USUARIOS", [
        ("Crear usuario", usuario_crear),
        ("Listar usuarios", mostrar_usuarios),
        ("Actualizar usuario", usuario_actualizar),
        ("Eliminar usuario", usuario_eliminar),
    ])



# TARJETAS
def tarjeta_crear():
    mostrar_tableros()
    mostrar_listas(pedir_int("ID del tablero (para ver sus listas): "))
    lista_id = pedir_int("ID de la lista: ")
    titulo = pedir_texto("Título: ")
    desc = pedir_texto("Descripción (opcional): ", False)
    fecha = pedir_fecha("Fecha límite AAAA-MM-DD (opcional): ")
    resp = None
    if confirmar("¿Asignar responsable?"):
        mostrar_usuarios()
        resp = pedir_int("ID del usuario: ")
    t = crud.crear_tarjeta(titulo, lista_id, desc, fecha, resp)
    if t:
        print(f"  Tarjeta creada con id {t.id}.")


def tarjeta_listar():
    lista_id = pedir_int("Filtrar por ID de lista (vacío = todas): ", False)
    mostrar_tarjetas(lista_id)


def tarjeta_listar_por_estado():
    mostrar_tarjetas(estado=pedir_estado())


def tarjeta_detalle():
    id_ = pedir_int("ID de la tarjeta: ")
    t = crud.obtener_tarjeta(id_)
    if t is None:
        print("  No existe.")
        return
    print("\n  " + _fmt_tarjeta(t))
    print(f"  Descripción: {t.descripcion or '-'}")
    etiquetas = crud.listar_etiquetas_de_tarjeta(id_)
    print("  Etiquetas: " + (", ".join(e.nombre for e in etiquetas) or "-"))
    comentarios = crud.listar_comentarios(id_)
    print(f"  Comentarios ({len(comentarios)}):")
    for c in comentarios:
        print(f"    [{c.id}] {c.fechaCreacion}: {c.contenido}")


def tarjeta_actualizar():
    mostrar_tarjetas()
    id_ = pedir_int("ID de la tarjeta: ")
    if crud.obtener_tarjeta(id_) is None:
        print("  No existe.")
        return
    print("  (deja vacío lo que no quieras cambiar)")
    crud.actualizar_tarjeta(id_, pedir_texto("Nuevo título: ", False),
                            pedir_texto("Nueva descripción: ", False),
                            pedir_fecha("Nueva fecha límite AAAA-MM-DD: "))
    print("  Actualizada.")


def tarjeta_cambiar_estado():
    mostrar_tarjetas()
    id_ = pedir_int("ID de la tarjeta: ")
    if crud.obtener_tarjeta(id_) is None:
        print("  No existe.")
        return
    crud.cambiar_estado_tarjeta(id_, pedir_estado())
    print("  Estado actualizado.")


def tarjeta_mover():
    mostrar_tarjetas()
    id_ = pedir_int("ID de la tarjeta: ")
    if crud.obtener_tarjeta(id_) is None:
        print("  No existe.")
        return
    mostrar_tableros()
    mostrar_listas(pedir_int("ID del tablero (para ver sus listas): "))
    nueva = pedir_int("ID de la lista destino: ")
    if crud.obtener_lista(nueva) is None:
        print("  La lista no existe.")
        return
    crud.mover_tarjeta(id_, nueva)
    print("  Tarjeta movida.")


def tarjeta_asignar():
    mostrar_tarjetas()
    id_ = pedir_int("ID de la tarjeta: ")
    if crud.obtener_tarjeta(id_) is None:
        print("  No existe.")
        return
    mostrar_usuarios()
    uid = pedir_int("ID del usuario responsable: ")
    if crud.obtener_usuario(uid) is None:
        print("  El usuario no existe.")
        return
    crud.asignar_responsable(id_, uid)
    print("  Responsable asignado.")


def tarjeta_quitar_responsable():
    mostrar_tarjetas()
    id_ = pedir_int("ID de la tarjeta: ")
    crud.quitar_responsable(id_)
    print("  Responsable quitado.")


def tarjeta_eliminar():
    mostrar_tarjetas()
    _eliminar_generico("tarjeta", crud.obtener_tarjeta, crud.eliminar_tarjeta,
                       "Se borrarán sus comentarios y etiquetas asociadas.")


def menu_tarjetas():
    ejecutar_menu("TARJETAS", [
        ("Crear tarjeta", tarjeta_crear),
        ("Listar tarjetas (todas o por lista)", tarjeta_listar),
        ("Listar tarjetas por estado", tarjeta_listar_por_estado),
        ("Ver detalle de una tarjeta", tarjeta_detalle),
        ("Actualizar título/descripción/fecha", tarjeta_actualizar),
        ("Cambiar estado", tarjeta_cambiar_estado),
        ("Mover a otra lista", tarjeta_mover),
        ("Asignar responsable", tarjeta_asignar),
        ("Quitar responsable", tarjeta_quitar_responsable),
        ("Eliminar tarjeta", tarjeta_eliminar),
    ])



# ETIQUETAS
def etiqueta_crear():
    e = crud.crear_etiqueta(pedir_texto("Nombre: "),
                            pedir_texto("Color (ej: rojo o #ff0000): "))
    print(f"  Etiqueta creada con id {e.id}.")


def etiqueta_actualizar():
    mostrar_etiquetas()
    id_ = pedir_int("ID de la etiqueta: ")
    if crud.obtener_etiqueta(id_) is None:
        print("  No existe.")
        return
    print("  (deja vacío lo que no quieras cambiar)")
    crud.actualizar_etiqueta(id_, pedir_texto("Nuevo nombre: ", False),
                             pedir_texto("Nuevo color: ", False))
    print("  Actualizada.")


def etiqueta_eliminar():
    mostrar_etiquetas()
    _eliminar_generico("etiqueta", crud.obtener_etiqueta, crud.eliminar_etiqueta,
                       "Se quitará de todas las tarjetas.")


def menu_etiquetas():
    ejecutar_menu("ETIQUETAS", [
        ("Crear etiqueta", etiqueta_crear),
        ("Listar etiquetas", mostrar_etiquetas),
        ("Actualizar etiqueta", etiqueta_actualizar),
        ("Eliminar etiqueta", etiqueta_eliminar),
    ])



# COMENTARIOS
def comentario_crear():
    mostrar_tarjetas()
    tid = pedir_int("ID de la tarjeta: ")
    c = crud.crear_comentario(pedir_texto("Comentario: "), tid)
    if c:
        print(f"  Comentario creado con id {c.id}.")


def comentario_listar():
    tid = pedir_int("ID de la tarjeta: ")
    _mostrar("Comentarios", crud.listar_comentarios(tid),
             lambda c: f"[{c.id}] {c.fechaCreacion}: {c.contenido}")


def comentario_actualizar():
    comentario_listar()
    id_ = pedir_int("ID del comentario a editar: ")
    if crud.actualizar_comentario(id_, pedir_texto("Nuevo contenido: ")):
        print("  Actualizado.")
    else:
        print("  No existe.")


def comentario_eliminar():
    comentario_listar()
    id_ = pedir_int("ID del comentario a eliminar: ")
    if confirmar(f"¿Eliminar comentario {id_}?"):
        print("  Eliminado." if crud.eliminar_comentario(id_) else "  No existe.")


def menu_comentarios():
    ejecutar_menu("COMENTARIOS", [
        ("Crear comentario", comentario_crear),
        ("Listar comentarios de una tarjeta", comentario_listar),
        ("Actualizar comentario", comentario_actualizar),
        ("Eliminar comentario", comentario_eliminar),
    ])



# MIEMBROS DE PROYECTO  (Proyecto_Usuario)
def miembro_agregar():
    mostrar_proyectos()
    pid = pedir_int("ID del proyecto: ")
    mostrar_usuarios()
    uid = pedir_int("ID del usuario: ")
    if crud.agregar_usuario_a_proyecto(pid, uid):
        print("  Usuario agregado al proyecto.")


def miembro_quitar():
    mostrar_proyectos()
    pid = pedir_int("ID del proyecto: ")
    _mostrar("Miembros", crud.listar_miembros(pid), lambda u: f"[{u.id}] {u.nombre}")
    uid = pedir_int("ID del usuario a quitar: ")
    print("  Quitado." if crud.quitar_usuario_de_proyecto(pid, uid) else "  No era miembro.")


def miembro_listar():
    mostrar_proyectos()
    pid = pedir_int("ID del proyecto: ")
    _mostrar("Miembros", crud.listar_miembros(pid),
             lambda u: f"[{u.id}] {u.nombre} <{u.email}>")


def menu_miembros():
    ejecutar_menu("MIEMBROS DE PROYECTO", [
        ("Agregar usuario a proyecto", miembro_agregar),
        ("Quitar usuario de proyecto", miembro_quitar),
        ("Listar miembros de un proyecto", miembro_listar),
    ])



# ETIQUETAS DE UNA TARJETA  (Tarjeta_Etiqueta)
def te_agregar():
    mostrar_tarjetas()
    tid = pedir_int("ID de la tarjeta: ")
    mostrar_etiquetas()
    eid = pedir_int("ID de la etiqueta: ")
    if crud.agregar_etiqueta_a_tarjeta(tid, eid):
        print("  Etiqueta agregada a la tarjeta.")


def te_quitar():
    tid = pedir_int("ID de la tarjeta: ")
    _mostrar("Etiquetas de la tarjeta", crud.listar_etiquetas_de_tarjeta(tid),
             lambda e: f"[{e.id}] {e.nombre}")
    eid = pedir_int("ID de la etiqueta a quitar: ")
    print("  Quitada." if crud.quitar_etiqueta_de_tarjeta(tid, eid) else "  La tarjeta no tenía esa etiqueta.")


def te_listar():
    tid = pedir_int("ID de la tarjeta: ")
    _mostrar("Etiquetas de la tarjeta", crud.listar_etiquetas_de_tarjeta(tid),
             lambda e: f"[{e.id}] {e.nombre} ({e.color})")


def menu_etiquetas_tarjeta():
    ejecutar_menu("ETIQUETAS DE UNA TARJETA", [
        ("Agregar etiqueta a tarjeta", te_agregar),
        ("Quitar etiqueta de tarjeta", te_quitar),
        ("Listar etiquetas de una tarjeta", te_listar),
    ])


# MENÚ PRINCIPAL
def menu_principal():
    ejecutar_menu("GESTIÓN DE PROYECTOS", [
        ("Proyectos", menu_proyectos),
        ("Tableros", menu_tableros),
        ("Listas", menu_listas),
        ("Tarjetas", menu_tarjetas),
        ("Usuarios", menu_usuarios),
        ("Etiquetas", menu_etiquetas),
        ("Comentarios", menu_comentarios),
        ("Miembros de proyecto", menu_miembros),
        ("Etiquetas de una tarjeta", menu_etiquetas_tarjeta),
        ("Ver todas las tablas", mostrar_todas_las_tablas),
    ], salida="Salir")
    print("\nHasta luego.")


if __name__ == "__main__":
    with database.connection_context():
        menu_principal()