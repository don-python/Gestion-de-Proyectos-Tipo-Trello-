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
- Contraseñas de al menos 8 caracteres, con una mayúscula, un número y un símbolo; se almacenan con BCrypt.
- Los hashes antiguos se conservan para no invalidar registros; pasan a BCrypt cuando se establece una nueva contraseña.
- Control de errores durante las operaciones con la base de datos.
- Prevención de asociaciones duplicadas mediante las restricciones de la base de datos.

## Estructura del proyecto

```text
proyecto/
├── datos/
│   ├── conexion.py
│   ├── model_base.py
│   ├── modelos/
│   │   └── models.py
│   ├── repositorio/
│   │   ├── operaciones.py
│   │   ├── proyectos.py
│   │   ├── tableros.py
│   │   ├── listas.py
│   │   ├── tarjetas.py
│   │   ├── usuarios.py
│   │   ├── etiquetas.py
│   │   ├── comentarios.py
│   │   └── relaciones.py
│   └── sql/
│       ├── trello.sql
│       └── 2026.10.20_15.02_crearusuario.sql
├── negocio/
│   ├── registros.py
│   ├── relaciones.py
│   └── usuarios.py
├── presentacion/
│   ├── interfaz.py
│   ├── menu.py
│   ├── proyecto_usuario.py
│   └── tarjeta_etiqueta.py
├── auxiliares/
│   ├── hasheo.py
│   ├── validaciones.py
│   └── probar_conexion.py
├── uml/
│   └── trello.drawio
├── .env
├── main.py
├── pyproject.toml
└── README.md
```
##  Base de datos

La base de datos utilizada se denomina `gestion_proyectos` y está implementada en MySQL.

Las tablas principales representan los proyectos, tableros, listas, tarjetas, usuarios, etiquetas y comentarios. También se utilizan tablas intermedias para gestionar las relaciones entre proyectos y usuarios, y entre tarjetas y etiquetas.

El archivo `datos/sql/trello.sql` contiene el script SQL del proyecto.

##  Instalación y ejecución

### 1. Requisitos previos

- Python instalado.
- MySQL en funcionamiento, por ejemplo, mediante XAMPP.
- phpMyAdmin para administrar la base de datos.

### 2. Instalar dependencias

Desde la carpeta raíz del proyecto, crear un entorno virtual e instalar el proyecto. Esto instala también las dependencias declaradas en `pyproject.toml` (`bcrypt`, `maskpass`, Peewee, MySQL y `python-dotenv`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

En el Símbolo del sistema de Windows, activar el entorno con:

```bat
.venv\Scripts\activate.bat
```

### 3. Configurar la base de datos

1. Iniciar MySQL desde XAMPP.
2. Abrir phpMyAdmin.
3. Crear la base de datos `gestion_proyectos` en phpMyAdmin e importar `datos/sql/trello.sql` para crear sus tablas.
4. Verificar en `.env` los valores de `DB_NAME`, `DB_HOST`, `DB_PORT`, `DB_USER` y `DB_PASSWORD` para que coincidan con la base local.

### 4. Ejecutar el programa

Desde la carpeta raíz del proyecto, con el entorno virtual activo, ejecutar:

```bash
python main.py
```

También se puede iniciar mediante el comando instalado:

```powershell
gestion-trello
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

**🟡 En desarrollo **

## 👨‍💻 Autores

**Fernando Prieto / Máximo Carrillos**
