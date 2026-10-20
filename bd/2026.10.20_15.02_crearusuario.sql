CREATE DATABASE IF NOT EXISTS gestion_proyectos;
CREATE USER 'trello_app'@'localhost' IDENTIFIED BY '1205fer';
GRANT ALL PRIVILEGES ON gestion_proyectos.* TO 'trello_app'@'localhost';
FLUSH PRIVILEGES;