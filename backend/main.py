from datetime import date
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from database import db
from schema import (
    LoginRequest, PropietarioCreate, MascotaCreate, TurnoCreate, TurnoUpdate
)
from auth import hash_password, crear_token_jwt, verificar_token

app = FastAPI(title="Sistema de Gestión de Turnos - Veterinaria Huellitas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# --- AUTENTICACIÓN JWT ---
@app.post("/login")
async def login(datos: LoginRequest):
    query = "SELECT * FROM usuario WHERE username = :username AND password_hash = :pwd"
    user = await db.fetch_one(
        query=query,
        values={"username": datos.username, "pwd": hash_password(datos.password)}
    )
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = crear_token_jwt(user["username"])
    return {"access_token": token, "nombre": user["nombreCompleto"]}

# --- CRUD PROPIETARIOS (R01) ---
@app.get("/propietarios")
async def listar_propietarios(usuario: str = Depends(verificar_token)):
    return await db.fetch_all("SELECT * FROM propietario ORDER BY apellido, nombre")

@app.post("/propietario", status_code=status.HTTP_201_CREATED)
async def crear_propietario(prop: PropietarioCreate, usuario: str = Depends(verificar_token)):
    query = """
    INSERT INTO propietario (dni, nombre, apellido, telefono, email, direccion)
    VALUES (:dni, :nombre, :apellido, :telefono, :email, :direccion)
    """
    try:
        await db.execute(query=query, values=prop.model_dump())
        return {"message": "Propietario registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error o DNI duplicado: {str(e)}")

@app.put("/propietario/{id}")
async def actualizar_propietario(id: int, prop: PropietarioCreate, usuario: str = Depends(verificar_token)):
    query = """
    UPDATE propietario
    SET dni = :dni, nombre = :nombre, apellido = :apellido,
        telefono = :telefono, email = :email, direccion = :direccion
    WHERE idPropietario = :id
    """
    res = await db.execute(query=query, values={**prop.model_dump(), "id": id})
    if res == 0:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return {"message": "Propietario modificado correctamente"}

@app.delete("/propietario/{id}")
async def eliminar_propietario(id: int, usuario: str = Depends(verificar_token)):
    try:
        res = await db.execute("DELETE FROM propietario WHERE idPropietario = :id", {"id": id})
        if res == 0:
            raise HTTPException(status_code=404, detail="Propietario no encontrado")
        return {"message": "Propietario eliminado"}
    except Exception:
        raise HTTPException(status_code=400, detail="No se puede eliminar: posee mascotas asociadas.")

# --- CRUD MASCOTAS (R02) ---
@app.get("/mascotas")
async def listar_mascotas(usuario: str = Depends(verificar_token)):
    query = """
    SELECT m.*, CONCAT(p.nombre, ' ', p.apellido) AS nombrePropietario
    FROM mascota m
    INNER JOIN propietario p ON m.idPropietario = p.idPropietario
    ORDER BY m.nombre
    """
    return await db.fetch_all(query)

@app.post("/mascota", status_code=status.HTTP_201_CREATED)
async def crear_mascota(mascota: MascotaCreate, usuario: str = Depends(verificar_token)):
    query = """
    INSERT INTO mascota (nombre, especie, raza, edad, idPropietario)
    VALUES (:nombre, :especie, :raza, :edad, :idPropietario)
    """
    await db.execute(query=query, values=mascota.model_dump())
    return {"message": "Mascota registrada correctamente"}

@app.put("/mascota/{id}")
async def actualizar_mascota(id: int, mascota: MascotaCreate, usuario: str = Depends(verificar_token)):
    query = """
    UPDATE mascota
    SET nombre = :nombre, especie = :especie, raza = :raza,
        edad = :edad, idPropietario = :idPropietario
    WHERE idMascota = :id
    """
    res = await db.execute(query=query, values={**mascota.model_dump(), "id": id})
    if res == 0:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return {"message": "Mascota actualizada"}

@app.delete("/mascota/{id}")
async def eliminar_mascota(id: int, usuario: str = Depends(verificar_token)):
    try:
        res = await db.execute("DELETE FROM mascota WHERE idMascota = :id", {"id": id})
        if res == 0:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        return {"message": "Mascota eliminada"}
    except Exception:
        raise HTTPException(status_code=400, detail="No se puede eliminar: posee turnos registrados.")

# --- GESTIÓN DE TURNOS CON STORED PROCEDURE ---
@app.get("/turnos")
async def consultar_turnos(fecha: date = None, usuario: str = Depends(verificar_token)):
    # Consulta SQL 1: Uso de múltiples INNER JOIN para agenda detallada 
    base_query = """
    SELECT t.idTurno, t.fecha, CAST(t.hora AS CHAR) AS hora, t.motivo, t.estado,
           m.idMascota, m.nombre AS mascota, m.especie,
           CONCAT(p.nombre, ' ', p.apellido) AS propietario, p.telefono
    FROM turno t
    INNER JOIN mascota m ON t.idMascota = m.idMascota
    INNER JOIN propietario p ON m.idPropietario = p.idPropietario
    """
    if fecha:
        query = base_query + " WHERE t.fecha = :fecha ORDER BY t.hora ASC"
        return await db.fetch_all(query=query, values={"fecha": fecha})
    query = base_query + " ORDER BY t.fecha DESC, t.hora ASC"
    return await db.fetch_all(query=query)

@app.post("/turno", status_code=status.HTTP_201_CREATED)
async def registrar_turno_sp(turno: TurnoCreate, usuario: str = Depends(verificar_token)):
    # Invoca el Stored Procedure transaccional
    call_sp = """
    CALL sp_registrar_turno(:fecha, :hora, :motivo, :idMascota, @res, @msg);
    """
    await db.execute(query=call_sp, values=turno.model_dump())
    out = await db.fetch_one("SELECT @res AS resultado, @msg AS mensaje;")
    if not out or out["resultado"] == 0:
        raise HTTPException(
            status_code=400,
            detail=out["mensaje"] if out else "No se pudo registrar el turno."
        )
    return {"message": out["mensaje"]}

@app.put("/turno/{id}")
async def modificar_turno(id: int, turno: TurnoUpdate, usuario: str = Depends(verificar_token)):
    # Verificar superposición si el turno no está cancelado 
    if turno.estado != "cancelado":
        choque = await db.fetch_one(
            """
            SELECT idTurno FROM turno
            WHERE fecha = :fecha AND hora = :hora AND estado != 'cancelado' AND idTurno != :id
            """,
            {"fecha": turno.fecha, "hora": turno.hora, "id": id}
        )
        if choque:
            raise HTTPException(status_code=400, detail="Horario ocupado por otro turno activo.")

    query = """
    UPDATE turno
    SET fecha = :fecha, hora = :hora, motivo = :motivo, estado = :estado, idMascota = :idMascota
    WHERE idTurno = :id
    """
    await db.execute(query=query, values={**turno.model_dump(), "id": id})
    return {"message": "Turno actualizado correctamente"}

@app.delete("/turno/{id}")
async def eliminar_turno(id: int, usuario: str = Depends(verificar_token)):
    res = await db.execute("DELETE FROM turno WHERE idTurno = :id", {"id": id})
    if res == 0:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return {"message": "Turno eliminado"}

# --- REPORTES ESPECIALES (GROUP BY Y SUBCONSULTAS) ---
@app.get("/reportes/estados")
async def reporte_por_estado(usuario: str = Depends(verificar_token)):
    # Consulta SQL 2: Agrupamiento con GROUP BY (R05)
    query = """
    SELECT estado, COUNT(*) AS totalTurnos
    FROM turno
    GROUP BY estado
    ORDER BY totalTurnos DESC
    """
    return await db.fetch_all(query)

@app.get("/reportes/propietarios-frecuentes")
async def reporte_propietarios_frecuentes(usuario: str = Depends(verificar_token)):
    # Consulta SQL 3: Subconsulta (Subquery) combinada con INNER JOIN y GROUP BY
    query = """
    SELECT p.dni, CONCAT(p.nombre, ' ', p.apellido) AS propietario, p.telefono,
           COUNT(t.idTurno) AS cantidadTurnos
    FROM propietario p
    INNER JOIN mascota m ON p.idPropietario = m.idPropietario
    INNER JOIN turno t ON m.idMascota = t.idMascota
    GROUP BY p.idPropietario, p.dni, p.nombre, p.apellido, p.telefono
    HAVING COUNT(t.idTurno) >= (
        SELECT AVG(conteo) FROM (
            SELECT COUNT(t2.idTurno) AS conteo
            FROM mascota m2
            INNER JOIN turno t2 ON m2.idMascota = t2.idMascota
            GROUP BY m2.idPropietario
        ) AS subtabla
    )
    ORDER BY cantidadTurnos DESC
    """
    return await db.fetch_all(query)
