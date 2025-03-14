CREATE DATABASE IF NOT EXISTS mcdonalddatabase;
USE mcdonalddatabase;

CREATE TABLE IF NOT EXISTS categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    imagen VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(5,2) DEFAULT 0 CHECK (descuento >= 0 AND descuento <= 100),
    precio_final DECIMAL(10,2) GENERATED ALWAYS AS (precio - (precio * (descuento / 100))) STORED,
    imagen VARCHAR(255),
    stock INT DEFAULT 0,
    disponible BOOLEAN DEFAULT TRUE,
    rating DECIMAL(3,2) DEFAULT 0,
    vendidos INT DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    tamaño ENUM('Pequeño', 'Mediano', 'Grande'),
    ingredientes TEXT,
    categoria_id INT NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categoria(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50),
    tipo_documento ENUM('DNI', 'Pasaporte', 'Cedula', 'Otro') NOT NULL,
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    pais_origen VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    rol VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS sucursal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    direccion VARCHAR(255) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    horario_atencion VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS empleado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    cargo ENUM('Cajero', 'Cocinero', 'Gerente', 'Supervisor', 'Limpieza', 'Repartidor') NOT NULL,
    sucursal_id INT NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    fecha_contratacion DATE NOT NULL,
    horario VARCHAR(50),
    estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    FOREIGN KEY (sucursal_id) REFERENCES sucursal(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    ciudad VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    empleado_id INT,
    sucursal_id INT NOT NULL,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    metodo_pago ENUM('Efectivo', 'Tarjeta', 'Transferencia') NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE SET NULL,
    FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE SET NULL,
    FOREIGN KEY (sucursal_id) REFERENCES sucursal(id) ON DELETE CASCADE
);

-- Tabla de promociones
CREATE TABLE IF NOT EXISTS promocion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    descuento DECIMAL(5,2) CHECK (descuento >= 0 AND descuento <= 100),
    precio_especial DECIMAL(10,2) CHECK (precio_especial >= 0),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
);

-- Tabla intermedia para la relación muchos a muchos entre productos y promociones
CREATE TABLE IF NOT EXISTS producto_promocion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    promocion_id INT NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES producto(id) ON DELETE CASCADE,
    FOREIGN KEY (promocion_id) REFERENCES promocion(id) ON DELETE CASCADE,
    UNIQUE (producto_id, promocion_id) -- Evita duplicados
);

INSERT IGNORE INTO categoria (nombre, imagen) VALUES
    ('Hamburguesas', 'img/hamburguesa.png'),
    ('Papas Fritas', 'img/papas.png'),
    ('Bebidas', 'img/bebidas.png'),
    ('Postres', 'img/postres.png'),
    ('Combos', 'img/combos.png'),
    ('Desayunos', 'img/desayunos.png');

INSERT INTO producto (nombre, descripcion, precio, imagen, categoria_id)
SELECT 'Big Mac', 'Hamburguesa con carne de res y salsa especial', 5.99, 'img/bigmac.png', id FROM categoria WHERE nombre='Hamburguesas'
UNION ALL
SELECT 'McNuggets', 'Porción de 10 piezas de nuggets de pollo', 4.99, 'img/nuggets.png', id FROM categoria WHERE nombre='Combos'
UNION ALL
SELECT 'Papas Grandes', 'Papas fritas crujientes', 2.99, 'img/papas_grandes.png', id FROM categoria WHERE nombre='Papas Fritas'
UNION ALL
SELECT 'Coca Cola', 'Refresco de cola 500ml', 1.99, 'img/coca.png', id FROM categoria WHERE nombre='Bebidas'
UNION ALL
SELECT 'Sundae', 'Helado de vainilla con cobertura', 2.49, 'img/sundae.png', id FROM categoria WHERE nombre='Postres'
UNION ALL
SELECT 'McMuffin', 'Sandwich de huevo y queso', 3.49, 'img/mcmuffin.png', id FROM categoria WHERE nombre='Desayunos'
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

INSERT INTO sucursal (nombre, direccion, ciudad, telefono, horario_atencion) 
VALUES 
('Sucursal Centro', 'Av. Principal 123', 'Ciudad A', '555-1234', '08:00 - 22:00'),
('Sucursal Norte', 'Calle Secundaria 456', 'Ciudad B', '555-5678', '09:00 - 21:00');

INSERT INTO empleado (nombre, apellido, email, telefono, cargo, sucursal_id, salario, fecha_contratacion, horario, estado) 
VALUES 
('Juan', 'Pérez', 'juan.perez@email.com', '555-1111', 'Gerente', 1, 2500.00, '2024-01-15', '08:00 - 17:00', 'Activo'),
('Ana', 'López', 'ana.lopez@email.com', '555-2222', 'Cocinero', 1, 1800.00, '2023-11-10', '10:00 - 18:00', 'Activo'),
('Carlos', 'García', 'carlos.garcia@email.com', '555-3333', 'Repartidor', 2, 1200.00, '2024-02-05', '12:00 - 20:00', 'Activo');

INSERT INTO cliente (nombre, apellido, email, telefono, direccion, ciudad) 
VALUES 
('María', 'González', 'maria.gonzalez@email.com', '555-4444', 'Calle 5 #10-20', 'Ciudad A'),
('Pedro', 'Ramírez', 'pedro.ramirez@email.com', '555-5555', 'Carrera 12 #8-30', 'Ciudad B'),
('Sofía', 'Martínez', NULL, '555-6666', 'Av. Siempre Viva 742', 'Ciudad A');

INSERT INTO venta (cliente_id, empleado_id, sucursal_id, total, metodo_pago) 
VALUES 
(1, 1, 1, 45.50, 'Efectivo'),
(2, 2, 1, 30.75, 'Tarjeta'),
(3, 3, 2, 15.00, 'Transferencia');

-- DROP DATABASE mcdonalddatabase;