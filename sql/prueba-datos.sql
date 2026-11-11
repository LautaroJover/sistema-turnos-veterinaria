USE veterinaria_huellitas;

-- Usuario inicial: recepcion / password: admin123 (hash SHA-256 para simplicidad artesanal sin fallos de versión)
INSERT INTO usuario (username, password_hash, nombreCompleto, rol)
VALUES ('recepcion', SHA2('admin123', 256), 'Recepción Veterinaria Huellitas', 'recepcion');

INSERT INTO propietario (dni, nombre, apellido, telefono, email, direccion) VALUES
('35111222', 'Carlos', 'Gómez', '3804112233', 'carlos@mail.com', 'Av. San Martín 120'),
('38444555', 'Lucía', 'Fernández', '3804998877', 'lucia@mail.com', 'Belgrano 450');

INSERT INTO mascota (nombre, especie, raza, edad, idPropietario) VALUES
('Rocco', 'Perro', 'Labrador', 4, 1),
('Mishi', 'Gato', 'Siamés', 2, 1),
('Luna', 'Perro', 'Caniche', 6, 2);

INSERT INTO turno (fecha, hora, motivo, estado, idMascota) VALUES
(CURDATE(), '09:00:00', 'Control anual y vacunación', 'pendiente', 1),
(CURDATE(), '10:00:00', 'Consulta dermatológica', 'atendido', 2),
(CURDATE(), '11:00:00', 'Desparasitación', 'pendiente', 3);