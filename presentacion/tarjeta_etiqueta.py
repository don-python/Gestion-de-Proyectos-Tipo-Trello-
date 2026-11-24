from prettytable import PrettyTable

from negocio.relaciones import (
    asociar_etiqueta,
    desasociar_etiqueta,
    listar_asociaciones,
)


def menu_asociaciones():
    while True:
        tabla = PrettyTable()
        tabla.field_names = ["Opción", "Operación"]
        tabla.add_rows([
            ["1", "Listar asociaciones"],
            ["2", "Asociar etiqueta a tarjeta"],
            ["3", "Desasociar etiqueta de tarjeta"],
            ["0", "Volver"],
        ])
        print("\n=== GESTIÓN DE ETIQUETAS DE TARJETAS ===")
        print(tabla)
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            try:
                registros = listar_asociaciones()
                if registros:
                    for registro in registros:
                        print(f"Tarjeta ID: {registro.tarjeta_id} | Etiqueta ID: {registro.etiqueta_id}")
                else:
                    print("No hay etiquetas asociadas a tarjetas.")
            except Exception as error:
                print(f"Error al listar asociaciones: {error}")
        elif opcion in {"2", "3"}:
            tarjeta_id = input("ID de la tarjeta: ").strip()
            etiqueta_id = input("ID de la etiqueta: ").strip()
            if not (tarjeta_id.isdigit() and etiqueta_id.isdigit()):
                print("Debes ingresar ID numéricos válidos.")
            elif opcion == "2":
                if asociar_etiqueta(int(tarjeta_id), int(etiqueta_id)):
                    print("Etiqueta asociada correctamente.")
                else:
                    print("No se pudo asociar. Comprueba que existan los registros y que no esté duplicada.")
            elif desasociar_etiqueta(int(tarjeta_id), int(etiqueta_id)):
                print("Etiqueta desasociada correctamente.")
            else:
                print("No se encontró esa asociación.")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

        input("\nPresiona Enter para continuar...")
