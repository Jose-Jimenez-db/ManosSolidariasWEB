"""
Este archivo define los esquemas de validación para las entregas
alimentarias. Incluye los modelos utilizados para registrar, actualizar y
consultar la información de las entregas, garantizando que los datos
recibidos y enviados por la API cumplan con la estructura establecida.
"""

from datetime import date
from pydantic import BaseModel, ConfigDict


class EntregaAlimentariaCreateSchema(BaseModel):
    codigo_entrega: str
    identificacion_beneficiario: str
    codigo_recurso: str
    cantidad_entregada: int
    fecha: date
    responsable_entrega: str

    model_config = ConfigDict(from_attributes=True)


class EntregaAlimentariaSchema(BaseModel):
    codigo_entrega: str
    identificacion_beneficiario: str
    codigo_recurso: str
    cantidad_entregada: int
    fecha: date
    responsable_entrega: str
    valor_economico: float

    model_config = ConfigDict(from_attributes=True)


class EntregaAlimentariaUpdateSchema(BaseModel):
    fecha: date
    responsable_entrega: str
