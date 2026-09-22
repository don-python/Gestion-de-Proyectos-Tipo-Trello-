
CREATE DATABASE gestion_proyectos;

USE gestion_proyectos;

CREATE TABLE Proyecto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    fechaCreacion DATE NOT NULL
);

CREATE TABLE Tablero (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    proyecto_id INT NOT NULL UNIQUE,
    FOREIGN KEY (proyecto_id) REFERENCES Proyecto(id)
);

CREATE TABLE Lista (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    posicion INT NOT NULL,
    tablero_id INT NOT NULL,
    FOREIGN KEY (tablero_id) REFERENCES Tablero(id)
);

CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL
);

CREATE TABLE Tarjeta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion VARCHAR(500),
    fechaLimite DATE,
    estado ENUM(
        'PENDIENTE',
        'EN_PROGRESO',
        'COMPLETADA',
        'BLOQUEADA'
    ) NOT NULL DEFAULT 'PENDIENTE',
    lista_id INT NOT NULL,
    responsable_id INT NULL,
    FOREIGN KEY (lista_id) REFERENCES Lista(id),
    FOREIGN KEY (responsable_id) REFERENCES Usuario(id)
);

CREATE TABLE Etiqueta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    color VARCHAR(50) NOT NULL
);

CREATE TABLE Comentario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contenido VARCHAR(500) NOT NULL,
    fechaCreacion DATE NOT NULL,
    tarjeta_id INT NOT NULL,
    FOREIGN KEY (tarjeta_id) REFERENCES Tarjeta(id)
);

CREATE TABLE Proyecto_Usuario (
    proyecto_id INT NOT NULL,
    usuario_id INT NOT NULL,
    PRIMARY KEY (proyecto_id, usuario_id),
    FOREIGN KEY (proyecto_id) REFERENCES Proyecto(id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);

CREATE TABLE Tarjeta_Etiqueta (
    tarjeta_id INT NOT NULL,
    etiqueta_id INT NOT NULL,
    PRIMARY KEY (tarjeta_id, etiqueta_id),
    FOREIGN KEY (tarjeta_id) REFERENCES Tarjeta(id),
    FOREIGN KEY (etiqueta_id) REFERENCES Etiqueta(id)
);