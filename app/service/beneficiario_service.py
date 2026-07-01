"""
Este archivo implementa el servicio de beneficiarios. Se encarga de aplicar
las reglas de negocio y las validaciones necesarias antes de realizar las
operaciones relacionadas con los beneficiarios, utilizando el repositorio
para interactuar con la base de datos.
"""

from app.repository.beneficiario_repository import BeneficiarioRepository
from app.schema.beneficiario_schema import ALLOWED_PRIORIDAD


class BeneficiarioService:
    def __init__(self):
        self.repo = BeneficiarioRepository()

    def _validate_common_data(self, nombre_completo, comunidad, integrantes_hogar, prioridad_social):
        if nombre_completo.strip() == "":
            raise ValueError("El nombre completo no puede estar vacío.")
        if comunidad.strip() == "":
            raise ValueError("La comunidad no puede estar vacía.")
        if integrantes_hogar <= 0:
            raise ValueError("Los integrantes del hogar deben ser mayores a cero.")
        if prioridad_social not in ALLOWED_PRIORIDAD:
            raise ValueError("La prioridad social debe ser Alta, Media o Baja.")

    def create_beneficiario(self, identificacion, nombre_completo, comunidad, integrantes_hogar, prioridad_social):
        if identificacion.strip() == "":
            raise ValueError("La identificación no puede estar vacía.")
        if self.repo.get(identificacion):
            raise ValueError("Ya existe un beneficiario con esa identificación.")

        self._validate_common_data(nombre_completo, comunidad, integrantes_hogar, prioridad_social)

        return self.repo.create(
            identificacion.strip(),
            nombre_completo.strip(),
            comunidad.strip(),
            integrantes_hogar,
            prioridad_social
        )

    def get_beneficiario(self, identificacion):
        return self.repo.get(identificacion)

    def list_beneficiarios(self):
        return self.repo.get_all()

    def update_beneficiario(self, identificacion, nombre_completo, comunidad, integrantes_hogar, prioridad_social):
        beneficiario = self.repo.get(identificacion)
        if not beneficiario:
            return None

        self._validate_common_data(nombre_completo, comunidad, integrantes_hogar, prioridad_social)

        return self.repo.update(
            identificacion,
            nombre_completo.strip(),
            comunidad.strip(),
            integrantes_hogar,
            prioridad_social
        )

    def delete_beneficiario(self, identificacion):
        return self.repo.delete(identificacion)
