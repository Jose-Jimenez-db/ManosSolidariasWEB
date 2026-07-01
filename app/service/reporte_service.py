"""
Este archivo implementa el servicio de reportes del sistema. Se encarga de
obtener, procesar y organizar la información proveniente de los diferentes
repositorios para generar los reportes relacionados con beneficiarios,
recursos alimenticios y entregas realizadas.
"""

from app.repository.entrega_alimentaria_repository import EntregaAlimentariaRepository
from app.repository.recurso_alimenticio_repository import RecursoAlimenticioRepository
from app.repository.beneficiario_repository import BeneficiarioRepository


class ReporteService:
    def __init__(self):
        self.repo_entregas = EntregaAlimentariaRepository()
        self.repo_recursos = RecursoAlimenticioRepository()
        self.repo_beneficiarios = BeneficiarioRepository()

    def reporte_beneficiarios_por_comunidad(self):
        resultado = self.repo_beneficiarios.contar_por_comunidad()
        return [{"comunidad": comunidad, "cantidad_beneficiarios": cantidad} for comunidad, cantidad in resultado]

    def reporte_recursos_inventario_bajo(self, limite):
        try:
            limite = int(limite)
        except ValueError:
            raise ValueError("El límite mínimo debe ser un número entero válido.")

        recursos = self.repo_recursos.get_bajo_stock(limite)
        return [
            {
                "codigo_recurso": r.codigo_recurso,
                "nombre": r.nombre,
                "unidad_medida": r.unidad_medida,
                "cantidad_disponible": r.cantidad_disponible
            }
            for r in recursos
        ]

    def reporte_recursos_mas_entregados(self):
        totales = self.repo_entregas.total_entregado_por_recurso()
        resultado = []

        for codigo_recurso, cantidad_total in totales:
            recurso = self.repo_recursos.get(codigo_recurso)
            if recurso is not None:
                resultado.append({
                    "codigo_recurso": codigo_recurso,
                    "nombre": recurso.nombre,
                    "unidad_medida": recurso.unidad_medida,
                    "cantidad_total_entregada": cantidad_total
                })

        resultado.sort(key=lambda dato: dato["cantidad_total_entregada"], reverse=True)
        return resultado

    def reporte_costo_total_ayuda_distribuida(self):
        return {"costo_total_distribuido": self.repo_entregas.costo_total_distribuido()}
