from prettytable import PrettyTable

from datos.conexion import database
from datos.modelos.models import (
    Comentario,
    Etiqueta,
    Lista,
    Proyecto,
    Tablero,
    Tarjeta,
    Usuario,
)
from negocio.usuarios import buscar_usuario_por_rut
from presentacion.interfaz import menu_crud
from presentacion.proyecto_usuario import menu_participantes
from presentacion.tarjeta_etiqueta import menu_asociaciones


def flujo_buscar_usuario_por_rut():
    print("\n--- BUSCAR USUARIO POR RUT ---")
    rut = input("Ingresa el RUT del usuario (ej. 12.345.678-9 o 12345678-9): ").strip()
    try:
        usuario = buscar_usuario_por_rut(rut)
    except ValueError as err:
        print(f"Error: {err}")
        return

    if not usuario:
        print("No se encontró ningún usuario con ese RUT.")
        return

    tabla = PrettyTable()
    tabla.field_names = ["ID", "RUT", "Nombre", "Email"]
    tabla.add_row([usuario.id, usuario.rut, usuario.nombre, usuario.email])
    print("\nUsuario encontrado:")
    print(tabla)


def mostrar_menu():
    tabla = PrettyTable()
    tabla.field_names = ["Opción", "Operación"]
    tabla.add_rows([
        ["1", "Listar proyectos"],
        ["2", "Listar tableros"],
        ["3", "Listar listas"],
        ["4", "Listar usuarios"],
        ["5", "Listar tarjetas"],
        ["6", "Listar etiquetas"],
        ["7", "Listar comentarios"],
        ["8", "Gestionar participantes de proyectos"],
        ["9", "Gestionar etiquetas de tarjetas"],
        ["10", "Buscar usuario por RUT"],
        ["0", "Salir"],
    ])
    print("\n=== GESTIÓN DE PROYECTOS ===")
    print(tabla)


def main():
    acciones = {
        "1": lambda: menu_crud(Proyecto, "Proyectos"),
        "2": lambda: menu_crud(Tablero, "Tableros"),
        "3": lambda: menu_crud(Lista, "Listas"),
        "4": lambda: menu_crud(Usuario, "Usuarios"),
        "5": lambda: menu_crud(Tarjeta, "Tarjetas"),
        "6": lambda: menu_crud(Etiqueta, "Etiquetas"),
        "7": lambda: menu_crud(Comentario, "Comentarios"),
        "8": menu_participantes,
        "9": menu_asociaciones,
        "10": flujo_buscar_usuario_por_rut,
    }
    try:
        while True:
            mostrar_menu()
            opcion = input("Selecciona una opción: ").strip()
            if opcion == "0":
                print("Hasta pronto.")
                break
            accion = acciones.get(opcion)
            if accion:
                accion()
                input("\nPresiona Enter para continuar...")
            else:
                print("Opción no válida.")
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado.")
    finally:
        if not database.is_closed():
            database.close()
