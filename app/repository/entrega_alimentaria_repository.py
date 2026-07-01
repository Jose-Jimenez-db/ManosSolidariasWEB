"""
Este archivo implementa el repositorio de entregas alimentarias. Se encarga
de realizar las operaciones de acceso a la base de datos relacionadas con
las entregas, incluyendo el registro, consulta, actualización, eliminación
y la obtención de información utilizada para la generación de reportes del
sistema.
"""

from sqlalchemy import func
from app.config.database import SessionLocal
from app.entity.entrega_alimentaria import EntregaAlimentariaORM


class EntregaAlimentariaRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, codigo_entrega, identificacion_beneficiario, codigo_recurso,
               cantidad_entregada, fecha, responsable_entrega, valor_economico):
        entrega = EntregaAlimentariaORM(
            codigo_entrega=codigo_entrega,
            identificacion_beneficiario=identificacion_beneficiario,
            codigo_recurso=codigo_recurso,
            cantidad_entregada=cantidad_entregada,
            fecha=fecha,
            responsable_entrega=responsable_entrega,
            valor_economico=valor_economico
        )
        self.db.add(entrega)
        self.db.commit()
        return entrega

    def get(self, codigo_entrega):
        return self.db.query(EntregaAlimentariaORM).filter_by(codigo_entrega=codigo_entrega).first()

    def get_all(self):
        return self.db.query(EntregaAlimentariaORM).all()

    def update(self, codigo_entrega, fecha, responsable_entrega):
        entrega = self.get(codigo_entrega)
        if entrega:
            entrega.fecha = fecha
            entrega.responsable_entrega = responsable_entrega
            self.db.commit()
        return entrega

    def delete(self, codigo_entrega):
        entrega = self.get(codigo_entrega)
        if entrega:
            self.db.delete(entrega)
            self.db.commit()
        return entrega

    def total_entregado_por_recurso(self):
        rows = self.db.query(
            EntregaAlimentariaORM.codigo_recurso,
            func.sum(EntregaAlimentariaORM.cantidad_entregada)
        ).group_by(EntregaAlimentariaORM.codigo_recurso).all()
        return [(codigo_recurso, int(cantidad)) for codigo_recurso, cantidad in rows]

    def costo_total_distribuido(self):
        total = self.db.query(func.sum(EntregaAlimentariaORM.valor_economico)).scalar()
        return float(total) if total is not None else 0.0
