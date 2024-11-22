CREATE DATABASE IF NOT EXISTS app-crud-juego;
USE app-crud-juego;

CREATE TABLE IF NOT EXISTS juegos(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
);