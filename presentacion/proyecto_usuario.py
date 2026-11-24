from prettytable import PrettyTable

from negocio.relaciones import (
    agregar_participante,
    eliminar_participante,
    listar_participantes,
)


def menu_participantes():
    while True:
        tabla = PrettyTable()
        tabla.field_names = ["Opción", "Operación"]
        tabla.add_rows([
            ["1", "Listar participantes"],
            ["2", "Agregar participante"],
            ["3", "Eliminar participante"],
            ["0", "Volver"],
        ])
        print("\n=== GESTIÓN DE PARTICIPANTES ===")
        print(tabla)
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            try:
                registros = listar_participantes()
                if registros:
                    for registro in registros:
                        print(f"Proyecto ID: {registro.proyecto_id} | Usuario ID: {registro.usuario_id}")
                else:
                    print("No hay participantes registrados.")
            except Exception as error:
                print(f"Error al listar participantes: {error}")
        elif opcion in {"2", "3"}:
            proyecto_id = input("ID del proyecto: ").strip()
            usuario_id = input("ID del usuario: ").strip()
            if not (proyecto_id.isdigit() and usuario_id.isdigit()):
                print("Debes ingresar ID numéricos válidos.")
            elif opcion == "2":
                if agregar_participante(int(proyecto_id), int(usuario_id)):
                    print("Participante agregado correctamente.")
                else:
                    print("No se pudo agregar. Comprueba que existan los registros y que no esté duplicado.")
            elif eliminar_participante(int(proyecto_id), int(usuario_id)):
                print("Participante eliminado correctamente.")
            else:
                print("No se encontró esa relación.")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

        input("\nPresiona Enter para continuar...")
