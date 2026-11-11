CREATE DATABASE IF NOT EXISTS veterinaria_huellitas
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE veterinaria_huellitas;

-- 1. Tabla de Usuarios (Personal de recepción y administración - Supuesto S01)
CREATE TABLE usuario (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombreCompleto VARCHAR(100) NOT NULL,
    rol VARCHAR(30) NOT NULL DEFAULT 'recepcion'
) ENGINE=InnoDB;

-- 2. Tabla de Propietarios (Requerimiento R01)
CREATE TABLE propietario (
    idPropietario INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(15) NOT NULL UNIQUE,
    nombre VARCHAR(60) NOT NULL,
    apellido VARCHAR(60) NOT NULL,
    telefono VARCHAR(30) NOT NULL,
    email VARCHAR(100) DEFAULT NULL,
    direccion VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- 3. Tabla de Mascotas (Requerimiento R02)
CREATE TABLE mascota (
    idMascota INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    especie VARCHAR(40) NOT NULL,
    raza VARCHAR(60) DEFAULT 'Mestizo',
    edad INT NOT NULL CHECK (edad >= 0),
    idPropietario INT NOT NULL,
    CONSTRAINT fk_mascota_propietario 
        FOREIGN KEY (idPropietario) REFERENCES propietario(idPropietario)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 4. Tabla de Turnos (Requerimientos R03, R04, R05 y R06)
CREATE TABLE turno (
    idTurno INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo VARCHAR(200) NOT NULL,
    estado ENUM('pendiente', 'atendido', 'cancelado') NOT NULL DEFAULT 'pendiente',
    idMascota INT NOT NULL,
    CONSTRAINT fk_turno_mascota 
        FOREIGN KEY (idMascota) REFERENCES mascota(idMascota)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;