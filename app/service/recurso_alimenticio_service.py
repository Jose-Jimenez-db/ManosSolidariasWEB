"""
Este archivo implementa el servicio de recursos alimenticios. Se encarga de
aplicar las reglas de negocio y las validaciones necesarias antes de
realizar las operaciones relacionadas con los recursos, así como gestionar
las consultas sobre el inventario disponible mediante el repositorio.
"""

from app.repository.recurso_alimenticio_repository import RecursoAlimenticioRepository


class RecursoAlimenticioService:
    def __init__(self):
        self.repo = RecursoAlimenticioRepository()

    def _validate_common_data(self, nombre, categoria, unidad_medida, cantidad_disponible, costo_unitario):
        if nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacío.")
        if categoria.strip() == "":
            raise ValueError("La categoría no puede estar vacía.")
        if unidad_medida.strip() == "":
            raise ValueError("La unidad de medida no puede estar vacía.")
        if cantidad_disponible < 0:
            raise ValueError("La cantidad disponible no puede ser negativa.")
        if costo_unitario <= 0:
            raise ValueError("El costo unitario debe ser mayor que cero.")

    def create_recurso(self, codigo_recurso, nombre, categoria, unidad_medida, cantidad_disponible, costo_unitario):
        if codigo_recurso.strip() == "":
            raise ValueError("El código no puede estar vacío.")
        if self.repo.get(codigo_recurso):
            raise ValueError("Ya existe un recurso con ese código.")

        self._validate_common_data(nombre, categoria, unidad_medida, cantidad_disponible, costo_unitario)

        return self.repo.create(
            codigo_recurso.strip(),
            nombre.strip(),
            categoria.strip(),
            unidad_medida.strip(),
            cantidad_disponible,
            costo_unitario
        )

    def get_recurso(self, codigo_recurso):
        return self.repo.get(codigo_recurso)

    def list_recursos(self):
        return self.repo.get_all()

    def update_recurso(self, codigo_recurso, nombre, categoria, unidad_medida, cantidad_disponible, costo_unitario):
        recurso = self.repo.get(codigo_recurso)
        if not recurso:
            return None

        self._validate_common_data(nombre, categoria, unidad_medida, cantidad_disponible, costo_unitario)

        return self.repo.update(
            codigo_recurso,
            nombre.strip(),
            categoria.strip(),
            unidad_medida.strip(),
            cantidad_disponible,
            costo_unitario
        )

    def delete_recurso(self, codigo_recurso):
        return self.repo.delete(codigo_recurso)

    def list_by_categoria(self, categoria):
        return self.repo.get_by_categoria(categoria)

    def list_bajo_stock(self, limite):
        if limite < 0:
            raise ValueError("El límite no puede ser negativo.")
        return self.repo.get_bajo_stock(limite)
