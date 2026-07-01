"""
Este archivo define la entidad BeneficiarioORM, la cual representa la tabla
de beneficiarios en la base de datos. Contiene los atributos principales del
beneficiario y la relación con las entregas alimentarias registradas mediante
SQLAlchemy.
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.config.database import Base


class BeneficiarioORM(Base):
    __tablename__ = "beneficiarios_tb"

    identificacion = Column(String(20), primary_key=True)
    nombre_completo = Column(String(100), nullable=False)
    comunidad = Column(String(60), nullable=False)
    integrantes_hogar = Column(Integer, nullable=False)
    prioridad_social = Column(String(20), nullable=False)

    entregas = relationship("EntregaAlimentariaORM", back_populates="beneficiario")

    def __repr__(self):
        return (
            f"BeneficiarioORM(identificacion='{self.identificacion}', "
            f"nombre_completo='{self.nombre_completo}', comunidad='{self.comunidad}')"
        )
