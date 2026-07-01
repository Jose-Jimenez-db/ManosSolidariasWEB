"""
Este archivo define la entidad RecursoAlimenticioORM, la cual representa la
tabla de recursos alimenticios en la base de datos. Contiene la información
de cada recurso disponible y la relación con las entregas alimentarias
registradas mediante SQLAlchemy.
"""

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from app.config.database import Base


class RecursoAlimenticioORM(Base):
    __tablename__ = "recursos_alimenticios_tb"

    codigo_recurso = Column(String(20), primary_key=True)
    nombre = Column(String(60), nullable=False)
    categoria = Column(String(30), nullable=False)
    unidad_medida = Column(String(20), nullable=False)
    cantidad_disponible = Column(Integer, nullable=False)
    costo_unitario = Column(Float, nullable=False)

    entregas = relationship("EntregaAlimentariaORM", back_populates="recurso")

    def __repr__(self):
        return (
            f"RecursoAlimenticioORM(codigo_recurso='{self.codigo_recurso}', "
            f"nombre='{self.nombre}', categoria='{self.categoria}')"
        )
