"""
Este archivo define el esquema de validación para los datos de los
beneficiarios. Establece la estructura de la información que recibe y
devuelve la API, permitiendo validar los datos antes de realizar las
operaciones correspondientes.
"""

from pydantic import BaseModel, ConfigDict


ALLOWED_PRIORIDAD = {"Alta", "Media", "Baja"}


class BeneficiarioSchema(BaseModel):
    identificacion: str
    nombre_completo: str
    comunidad: str
    integrantes_hogar: int
    prioridad_social: str

    model_config = ConfigDict(from_attributes=True)
