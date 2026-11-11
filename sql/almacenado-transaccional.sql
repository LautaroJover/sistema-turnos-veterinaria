USE veterinaria_huellitas;

DELIMITER $$

CREATE PROCEDURE sp_registrar_turno(
    IN p_fecha DATE,
    IN p_hora TIME,
    IN p_motivo VARCHAR(200),
    IN p_idMascota INT,
    OUT p_resultado INT,
    OUT p_mensaje VARCHAR(255)
)
BEGIN
    DECLARE v_ocupado INT DEFAULT 0;
    DECLARE v_existe_mascota INT DEFAULT 0;

    -- Manejador de errores: ante cualquier fallo SQL revierte los cambios
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_resultado = 0;
        SET p_mensaje = 'Error interno en la transacción de base de datos.';
    END;

    START TRANSACTION;

    -- Validar que la mascota exista
    SELECT COUNT(*) INTO v_existe_mascota 
    FROM mascota 
    WHERE idMascota = p_idMascota;

    IF v_existe_mascota = 0 THEN
        ROLLBACK;
        SET p_resultado = 0;
        SET p_mensaje = 'La mascota seleccionada no existe.';
    ELSE
        -- Validar Requerimiento R06: Superposición de horario (solo turnos no cancelados)
        SELECT COUNT(*) INTO v_ocupado
        FROM turno
        WHERE fecha = p_fecha 
          AND hora = p_hora 
          AND estado != 'cancelado'
        FOR UPDATE;

        IF v_ocupado > 0 THEN
            ROLLBACK;
            SET p_resultado = 0;
            SET p_mensaje = 'Superposición detectada: Ya existe un turno activo en esa fecha y hora.';
        ELSE
            INSERT INTO turno (fecha, hora, motivo, estado, idMascota)
            VALUES (p_fecha, p_hora, p_motivo, 'pendiente', p_idMascota);

            COMMIT;
            SET p_resultado = 1;
            SET p_mensaje = 'Turno registrado exitosamente.';
        END IF;
    END IF;
END$$

DELIMITER ;