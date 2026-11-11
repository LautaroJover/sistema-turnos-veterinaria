# Sistema de Gestión de Turnos - Veterinaria Huellitas

**Trabajo Práctico Final - Metodología de Sistemas II**  
**Carrera:** Tecnicatura Universitaria en Programación - UTN  
**Stack Tecnológico:** MySQL · FastAPI (Python) · React (JavaScript)

---

## 1. Temática del Proyecto (Acta del Proyecto)

### Declaración del Problema y Oportunidad
La **Veterinaria Huellitas** administra sus turnos mediante WhatsApp, llamadas telefónicas y anotaciones manuales. Esta modalidad genera superposición de horarios, pérdida de información y dificultades operativas para consultar la agenda diaria en las áreas de recepción, administración de turnos y atención al cliente.

### Solución Propuesta
Desarrollar un sistema web interno, sencillo y seguro que permita al personal de recepción y administración registrar propietarios, mascotas y turnos, así como consultar la agenda diaria por fecha desde un único lugar centralizado.

### Alcance - Requerimientos Funcionales Macro
* **R01:** Registrar y modificar propietarios.
* **R02:** Registrar y modificar mascotas asociadas a un propietario.
* **R03:** Registrar, modificar y cancelar turnos indicando fecha, hora, mascota y motivo de consulta.
* **R04:** Consultar los turnos correspondientes a una fecha determinada.
* **R05:** Identificar el estado de cada turno como `pendiente`, `atendido` o `cancelado`.
* **R06:** Evitar la superposición de dos turnos activos en el mismo horario.

### Restricciones y Supuestos del Dominio
* **Restricción R01:** El alcance se limita exclusivamente a la gestión básica de propietarios, mascotas y turnos.
* **Restricción R02:** No incluye módulos de pagos, facturación, inventario, historia clínica completa ni aplicación móvil.
* **Supuesto S01:** El sistema es utilizado únicamente por el personal interno de recepción y administración de la veterinaria.
* **Supuesto S02:** Se opera con una única agenda general de turnos, sin asignación a múltiples profesionales.

---

## 2. Consignas del Trabajo Práctico Final y Cumplimiento Técnico

### Objetivo General
Diseñar y desarrollar una aplicación web Full Stack utilizando **MySQL**, **FastAPI** y **React** que brinde una solución funcional a una problemática real, aplicando separación de responsabilidades en capas y código artesanal.