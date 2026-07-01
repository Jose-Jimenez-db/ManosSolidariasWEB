"""
Este archivo implementa el repositorio de beneficiarios. Se encarga de
realizar las operaciones de acceso a la base de datos relacionadas con los
beneficiarios, incluyendo el registro, consulta, actualización, eliminación
y la obtención de información utilizada en los reportes del sistema.
"""

from sqlalchemy import func
from app.config.database import SessionLocal
from app.entity.beneficiario import BeneficiarioORM


class BeneficiarioRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, identificacion, nombre_completo, comunidad, integrantes_hogar, prioridad_social):
        beneficiario = BeneficiarioORM(
            identificacion=identificacion,
            nombre_completo=nombre_completo,
            comunidad=comunidad,
            integrantes_hogar=integrantes_hogar,
            prioridad_social=prioridad_social
        )
        self.db.add(beneficiario)
        self.db.commit()
        return beneficiario

    def get(self, identificacion):
        return self.db.query(BeneficiarioORM).filter_by(identificacion=identificacion).first()

    def get_all(self):
        return self.db.query(BeneficiarioORM).all()

    def update(self, identificacion, nombre_completo, comunidad, integrantes_hogar, prioridad_social):
        beneficiario = self.get(identificacion)
        if beneficiario:
            beneficiario.nombre_completo = nombre_completo
            beneficiario.comunidad = comunidad
            beneficiario.integrantes_hogar = integrantes_hogar
            beneficiario.prioridad_social = prioridad_social
            self.db.commit()
        return beneficiario

    def delete(self, identificacion):
        beneficiario = self.get(identificacion)
        if beneficiario:
            self.db.delete(beneficiario)
            self.db.commit()
        return beneficiario

    def contar_por_comunidad(self):
        rows = self.db.query(
            BeneficiarioORM.comunidad, func.count(BeneficiarioORM.identificacion)
        ).group_by(BeneficiarioORM.comunidad).all()
        return [(comunidad, int(cantidad)) for comunidad, cantidad in rows]
