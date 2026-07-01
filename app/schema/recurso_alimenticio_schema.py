"""
Este archivo define el esquema de validación para los recursos alimenticios.
Establece la estructura de los datos que la API recibe y devuelve durante
las operaciones relacionadas con el inventario de recursos, asegurando la
consistencia y validez de la información.
"""

from pydantic import BaseModel, ConfigDict


class RecursoAlimenticioSchema(BaseModel):
    codigo_recurso: str
    nombre: str
    categoria: str
    unidad_medida: str
    cantidad_disponible: int
    costo_unitario: float

    model_config = ConfigDict(from_attributes=True)
