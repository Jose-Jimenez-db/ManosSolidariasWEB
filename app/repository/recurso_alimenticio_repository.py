"""
Este archivo implementa el repositorio de recursos alimenticios. Se encarga
de realizar las operaciones de acceso a la base de datos relacionadas con
los recursos, incluyendo el registro, consulta, actualización, eliminación,
el control del inventario disponible y la obtención de información para los
reportes del sistema.
"""

from app.config.database import SessionLocal
from app.entity.recurso_alimenticio import RecursoAlimenticioORM


class RecursoAlimenticioRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, codigo_recurso, nombre, categoria, unidad_medida, cantidad_disponible, costo_unitario):
        recurso = RecursoAlimenticioORM(
            codigo_recurso=codigo_recurso,
            nombre=nombre,
            categoria=categoria,
            unidad_medida=unidad_medida,
            cantidad_disponible=cantidad_disponible,
            costo_unitario=costo_unitario
        )
        self.db.add(recurso)
        self.db.commit()
        self.db.refresh(recurso)
        return recurso

    def get(self, codigo_recurso):
        return self.db.query(RecursoAlimenticioORM).filter_by(codigo_recurso=codigo_recurso).first()

    def get_all(self):
        return self.db.query(RecursoAlimenticioORM).all()

    def update(self, codigo_recurso, nombre, categoria, unidad_medida, cantidad_disponible, costo_unitario):
        recurso = self.get(codigo_recurso)
        if recurso:
            recurso.nombre = nombre
            recurso.categoria = categoria
            recurso.unidad_medida = unidad_medida
            recurso.cantidad_disponible = cantidad_disponible
            recurso.costo_unitario = costo_unitario
            self.db.commit()
        return recurso

    def delete(self, codigo_recurso):
        recurso = self.get(codigo_recurso)
        if recurso:
            self.db.delete(recurso)
            self.db.commit()
        return recurso

    def get_by_categoria(self, categoria):
        return self.db.query(RecursoAlimenticioORM).filter(
            RecursoAlimenticioORM.categoria.ilike(categoria)
        ).all()

    def descontar_cantidad(self, codigo_recurso, cantidad):
        recurso = self.get(codigo_recurso)
        if recurso:
            recurso.cantidad_disponible -= cantidad
            self.db.commit()
        return recurso

    def restaurar_cantidad(self, codigo_recurso, cantidad):
        recurso = self.get(codigo_recurso)
        if recurso:
            recurso.cantidad_disponible += cantidad
            self.db.commit()
        return recurso

    def get_bajo_stock(self, limite):
        return self.db.query(RecursoAlimenticioORM).filter(
            RecursoAlimenticioORM.cantidad_disponible < limite
        ).all()
