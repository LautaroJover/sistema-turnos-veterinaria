from typing import OptionalLiteral, Optional
from datetime import date, time
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)

class PropietarioCreate(BaseModel):
    dni: str = Field(..., min_length=7, max_length=15)
    nombre: str = Field(..., min_length=2, max_length=60)
    apellido: str = Field(..., min_length=2, max_length=60)
    telefono: str = Field(..., min_length=6, max_length=30)
    email: Optional[str] = Field(None, max_length=100)
    direccion: str = Field(..., min_length=4, max_length=150)

class MascotaCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=60)
    especie: str = Field(..., min_length=2, max_length=40)
    raza: Optional[str] = Field("Mestizo", max_length=60)
    edad: int = Field(..., ge=0, le=40)
    idPropietario: int = Field(..., gt=0)

class TurnoCreate(BaseModel):
    fecha: date
    hora: time
    motivo: str = Field(..., min_length=4, max_length=200)
    idMascota: int = Field(..., gt=0)

class TurnoUpdate(BaseModel):
    fecha: date
    hora: time
    motivo: str = Field(..., min_length=4, max_length=200)
    estado: str = Field(..., pattern="^(pendiente|atendido|cancelado)$")
    idMascota: int = Field(..., gt=0)