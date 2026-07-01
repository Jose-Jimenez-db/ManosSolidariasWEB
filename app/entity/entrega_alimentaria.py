"""
Este archivo define la entidad EntregaAlimentariaORM, la cual representa la
tabla de entregas alimentarias en la base de datos. Contiene la información
de cada entrega realizada y las relaciones con los beneficiarios y recursos
alimenticios mediante claves foráneas y SQLAlchemy.
"""

from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base


class EntregaAlimentariaORM(Base):
    __tablename__ = "entregas_alimentarias_tb"

    codigo_entrega = Column(String(20), primary_key=True)
    identificacion_beneficiario = Column(
        String(20), ForeignKey("beneficiarios_tb.identificacion"), nullable=False
    )
    codigo_recurso = Column(
        String(20), ForeignKey("recursos_alimenticios_tb.codigo_recurso"), nullable=False
    )
    cantidad_entregada = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)
    responsable_entrega = Column(String(60), nullable=False)
    valor_economico = Column(Float, nullable=False)

    beneficiario = relationship("BeneficiarioORM", back_populates="entregas")
    recurso = relationship("RecursoAlimenticioORM", back_populates="entregas")

    def __repr__(self):
        return (
            f"EntregaAlimentariaORM(codigo_entrega='{self.codigo_entrega}', "
            f"beneficiario='{self.identificacion_beneficiario}', "
            f"recurso='{self.codigo_recurso}')"
        )
