
from datetime import date
from crud.proyectos import crear_proyecto, listar_proyectos

if __name__ == "__main__":
    print("=== PRUEBA: CREAR PROYECTO ===")

    proyecto = crear_proyecto({
        "nombre": "Proyecto de prueba",
        "descripcion": "Registro creado para probar el CRUD",
        "fecha_creacion": date.today()
    })

    if proyecto:
        print("\n=== PRUEBA: LISTAR PROYECTOS ===")
        proyectos = listar_proyectos()
        print(f"\nProyectos encontrados: {len(proyectos)}")
