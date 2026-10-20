
from orm.models import database

try:
    database.connect()
    database.execute_sql("SELECT 1")
    print("Conexión exitosa con la base de datos.")

    print("Base de datos:", database.database)
    print("Servidor:", database.connect_params["host"])

except Exception as error:
    print("Error al conectar con la base de datos:")
    print(error)

finally:
    if not database.is_closed():
        database.close()
