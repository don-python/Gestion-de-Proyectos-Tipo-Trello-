# Gestión de Proyectos — Tipo Trello

Proyecto académico de **Programación Orientada a Objetos (POO)** que consiste en desarrollar un sistema de gestión de proyectos inspirado en herramientas como Trello, utilizando Python y una base de datos MySQL.

##  Objetivo

Permitir la administración de proyectos y la organización de tareas mediante tableros, listas y tarjetas, relacionando usuarios, etiquetas y comentarios.

##  Tecnologías utilizadas

- **Python:** lenguaje de programación.
- **Peewee ORM:** interacción entre Python y la base de datos.
- **MySQL:** almacenamiento de la información.
- **phpMyAdmin:** administración de la base de datos.
- **PrettyTable:** presentación de información en tablas en la consola.
- **Git y GitHub:** control de versiones y almacenamiento del proyecto.
- **draw.io:** elaboración del diagrama de clases UML.

##  Funcionalidades implementadas

### Gestión de registros (CRUD)

El sistema permite realizar las operaciones básicas de creación, consulta, actualización y eliminación para las siguientes entidades:

- 📁 Proyectos
- 📋 Tableros
- 📝 Listas
- 🗂️ Tarjetas
- 👤 Usuarios
- 🏷️ Etiquetas
- 💬 Comentarios

### Gestión de relaciones

- **Participantes de proyectos:** permite asociar usuarios a proyectos, consultar las asociaciones y eliminarlas.
- **Etiquetas de tarjetas:** permite asociar etiquetas a tarjetas, consultar las asociaciones y eliminarlas.

### Validaciones y manejo de datos

- Validación de identificadores y tipos de datos ingresados.
- Validación de los estados permitidos para las tarjetas.
- Control de errores durante las operaciones con la base de datos.
- Prevención de asociaciones duplicadas mediante las restricciones de la base de datos.

## 📂 Estructura del proyecto

```text
Gestion-de-Proyectos-Tipo-Trello/
├── bd/
│   └── trello.sql
├── crud/
│   ├── __init__.py
│   ├── comentarios.py
│   ├── etiquetas.py
│   ├── interfaz.py
│   ├── listas.py
│   ├── operaciones.py
│   ├── proyectos.py
│   ├── proyecto_usuario.py
│   ├── tableros.py
│   ├── tarjetas.py
│   ├── tarjeta_etiqueta.py
│   └── usuarios.py
├── orm/
│   ├── __init__.py
│   └── models.py
├── uml/
│   └── trello.drawio
├── main.py
├── probar_conexion.py
├── README.md
└── .gitignore
```

##  Base de datos

La base de datos utilizada se denomina `gestion_proyectos` y está implementada en MySQL.

Las tablas principales representan los proyectos, tableros, listas, tarjetas, usuarios, etiquetas y comentarios. También se utilizan tablas intermedias para gestionar las relaciones entre proyectos y usuarios, y entre tarjetas y etiquetas.

El archivo `bd/trello.sql` contiene el script SQL del proyecto.

##  Instalación y ejecución

### 1. Requisitos previos

- Python instalado.
- MySQL en funcionamiento, por ejemplo, mediante XAMPP.
- phpMyAdmin para administrar la base de datos.

### 2. Instalar dependencias

Desde una terminal, ejecutar:

```bash
pip install peewee pymysql prettytable
```

### 3. Configurar la base de datos

1. Iniciar MySQL desde XAMPP.
2. Abrir phpMyAdmin.
3. Crear o importar la base de datos `gestion_proyectos` utilizando el archivo `bd/trello.sql`.
4. Verificar que las credenciales de conexión configuradas en `orm/models.py` coincidan con el entorno local.

### 4. Ejecutar el programa

Desde la carpeta raíz del proyecto, ejecutar:

```bash
python main.py
```

El programa mostrará un menú principal desde el cual se puede acceder a las opciones de gestión de registros y asociaciones.

##  Pruebas realizadas

Se verificó el funcionamiento de los menús y submenús, incluyendo:

- Creación, consulta, búsqueda, actualización y eliminación de registros.
- Asociación y eliminación de participantes de proyectos.
- Asociación y eliminación de etiquetas de tarjetas.
- Consulta de las asociaciones registradas.
- Validación de asociaciones duplicadas.

##  Estado actual

**Estado: funcional en entorno local, en etapa de revisión y mejora.**

Las operaciones CRUD y la gestión de asociaciones fueron probadas satisfactoriamente. El proyecto puede continuar con la revisión de la consistencia entre el modelo UML, los modelos ORM y la estructura de la base de datos.

## Diseño UML

El archivo `uml/trello.drawio` contiene el diagrama de clases del proyecto, utilizado como referencia para representar las entidades, sus atributos y las relaciones del sistema.


##  Herramientas utilizadas

*  **draw.io** — Diseño de diagramas UML
*  **GitHub** — Almacenamiento y seguimiento del proyecto
*  **Git** — Control de versiones
*  **Xampp** - Servicio de hosting local

---

##  Estado actual

**🟡 En desarrollo — Etapa de diseño UML**

## 👨‍💻 Autores

**Fernando Prieto / Máximo Carrillos**
