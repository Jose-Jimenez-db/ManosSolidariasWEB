"""
Este archivo implementa el servicio de entregas alimentarias. Se encarga de
aplicar las reglas de negocio y las validaciones necesarias antes de
registrar, consultar, actualizar o eliminar entregas, además de gestionar
la disponibilidad de los recursos alimenticios mediante el inventario.
"""

from app.repository.entrega_alimentaria_repository import EntregaAlimentariaRepository
from app.repository.beneficiario_repository import BeneficiarioRepository
from app.repository.recurso_alimenticio_repository import RecursoAlimenticioRepository


class EntregaAlimentariaService:
    def __init__(self):
        self.repo = EntregaAlimentariaRepository()
        self.repo_beneficiarios = BeneficiarioRepository()
        self.repo_recursos = RecursoAlimenticioRepository()

    def create_entrega(self, codigo_entrega, identificacion_beneficiario, codigo_recurso,
                        cantidad_entregada, fecha, responsable_entrega):
        if codigo_entrega.strip() == "":
            raise ValueError("El código de entrega no puede estar vacío.")
        if self.repo.get(codigo_entrega):
            raise ValueError("Ya existe una entrega con ese código.")
        if cantidad_entregada <= 0:
            raise ValueError("La cantidad entregada debe ser mayor que cero.")
        if responsable_entrega.strip() == "":
            raise ValueError("El responsable de la entrega no puede estar vacío.")

        beneficiario = self.repo_beneficiarios.get(identificacion_beneficiario)
        if not beneficiario:
            raise ValueError("El beneficiario indicado no existe.")

        recurso = self.repo_recursos.get(codigo_recurso)
        if not recurso:
            raise ValueError("El recurso indicado no existe.")

        if recurso.cantidad_disponible < cantidad_entregada:
            raise ValueError(
                f"No hay suficiente disponibilidad. Disponible: {recurso.cantidad_disponible}"
            )

        valor_economico = round(cantidad_entregada * recurso.costo_unitario, 2)

        entrega = self.repo.create(
            codigo_entrega.strip(),
            identificacion_beneficiario,
            codigo_recurso,
            cantidad_entregada,
            fecha,
            responsable_entrega.strip(),
            valor_economico
        )

        self.repo_recursos.descontar_cantidad(codigo_recurso, cantidad_entregada)

        return entrega

    def get_entrega(self, codigo_entrega):
        return self.repo.get(codigo_entrega)

    def list_entregas(self):
        return self.repo.get_all()

    def update_entrega(self, codigo_entrega, fecha, responsable_entrega):
        if responsable_entrega.strip() == "":
            raise ValueError("El responsable de la entrega no puede estar vacío.")
        return self.repo.update(codigo_entrega, fecha, responsable_entrega.strip())

    def delete_entrega(self, codigo_entrega):
        entrega = self.repo.get(codigo_entrega)
        if entrega:
            self.repo_recursos.restaurar_cantidad(entrega.codigo_recurso, entrega.cantidad_entregada)
        return self.repo.delete(codigo_entrega)
