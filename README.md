# 📋 Gestión De Proyecto Tipo Trello

> Proyecto del ramo **Programación Orientada a Objetos (POO)** enfocado en el análisis y diseño de una solución mediante diagramas UML.

---

## 📌 Sobre el proyecto

El proyecto consiste en diseñar una solución para una organización que necesita gestionar proyectos mediante **tableros visuales**.

Cada proyecto puede contar con un tablero donde los usuarios organizan el trabajo mediante **listas y tarjetas**.

Las tarjetas representan tareas y contienen información como:

* 📝 Título
* 📄 Descripción
* 📅 Fecha límite
* 🔄 Estado
* 🏷️ Etiquetas
* 💬 Comentarios
* 👤 Responsable

Además, un proyecto puede contar con varios usuarios participantes y un usuario puede participar en distintos proyectos.

---

## 🎯 Objetivo

El objetivo de esta actividad es aplicar fundamentos de **Programación Orientada a Objetos** mediante el análisis de la problemática y la elaboración de un **diagrama de clases UML**.

El diseño busca representar de manera clara y coherente:

* Las clases principales del sistema.
* Sus atributos y características.
* Los métodos y responsabilidades.
* La visibilidad de sus elementos.
* Las relaciones entre las clases.
* Las multiplicidades correspondientes.
* Las enumeraciones necesarias para representar información con valores definidos.

---

## 🧩 Clases identificadas

A partir del análisis de la problemática se han identificado las siguientes clases:

| Clase           | Descripción                                                  |
| :-------------- | :----------------------------------------------------------- |
| 📁 `Proyecto`   | Representa un proyecto que se desea gestionar.               |
| 📋 `Tablero`    | Permite organizar visualmente el trabajo de un proyecto.     |
| 📝 `Lista`      | Organiza las tarjetas dentro de un tablero.                  |
| 🗂️ `Tarjeta`   | Representa una tarea del proyecto.                           |
| 👤 `Usuario`    | Representa a los participantes y responsables de las tareas. |
| 🏷️ `Etiqueta`  | Permite clasificar y organizar las tarjetas.                 |
| 💬 `Comentario` | Contiene información adicional asociada a una tarjeta.       |

---

## 🔢 Enumeración `Estado`

Para representar los diferentes estados que puede tener una tarjeta se utiliza la enumeración `Estado`.

Los valores definidos son:

```text
PENDIENTE
EN_PROGRESO
COMPLETADA
BLOQUEADA
```

La utilización de una enumeración permite trabajar con un conjunto de valores previamente definidos y mantener consistencia en el estado de las tarjetas.

---

## 🔗 Relaciones principales

El modelo considera las relaciones estructurales entre los diferentes elementos del sistema.

De forma general, la organización del modelo es:

```text
Proyecto
   │
   └── Tablero
         │
         └── Lista
               │
               └── Tarjeta
                    ├── Usuario
                    ├── Etiqueta
                    ├── Comentario
                    └── Estado
```

También se considera la relación entre **Proyecto y Usuario**, debido a que un proyecto puede contar con varios participantes y un usuario puede participar en distintos proyectos.

---

## 📐 Diagrama de clases UML

El proyecto se encuentra actualmente en la etapa de **análisis, diseño y refinamiento del modelo UML**.

El diagrama considera:

* Clases
* Atributos
* Métodos
* Visibilidad
* Relaciones
* Multiplicidades
* Enumeraciones
* Responsabilidades de cada clase

El modelo será revisado y refinado progresivamente para asegurar que represente correctamente la problemática planteada.

---

## 🛠️ Herramientas utilizadas

* 📐 **draw.io** — Diseño de diagramas UML
* 🐙 **GitHub** — Almacenamiento y seguimiento del proyecto
* 🌱 **Git** — Control de versiones

---

## 🚧 Estado actual

**🟡 En desarrollo — Etapa de diseño UML**

### Progreso

* [x] Análisis de la problemática
* [x] Identificación de clases
* [x] Identificación de atributos
* [x] Identificación de métodos
* [x] Identificación de relaciones
* [x] Definición inicial de multiplicidades
* [x] Incorporación de enumeración `Estado`
* [ ] Revisión y refinamiento del diagrama
* [ ] Finalización del modelo UML

## 👨‍💻 Autores

**Fernando Prieto / Máximo Carrillos**
