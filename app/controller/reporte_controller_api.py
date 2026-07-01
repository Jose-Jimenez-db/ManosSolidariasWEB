"""
Este archivo implementa el controlador de reportes del sistema. Define los
endpoints encargados de generar y devolver los diferentes reportes
disponibles, delegando el procesamiento de la información al servicio
correspondiente y controlando las respuestas enviadas por la API.
"""

from fastapi import APIRouter, HTTPException, Query

from app.service.reporte_service import ReporteService


router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/beneficiarios-por-comunidad")
def reporte_beneficiarios_por_comunidad():
    service = ReporteService()

    return service.reporte_beneficiarios_por_comunidad()


@router.get("/inventario-bajo")
def reporte_recursos_inventario_bajo(limite: int = Query(..., ge=0)):
    service = ReporteService()

    try:
        return service.reporte_recursos_inventario_bajo(limite)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/recursos-mas-entregados")
def reporte_recursos_mas_entregados():
    service = ReporteService()

    return service.reporte_recursos_mas_entregados()


@router.get("/costo-total-distribuido")
def reporte_costo_total_ayuda_distribuida():
    service = ReporteService()

    return service.reporte_costo_total_ayuda_distribuida()
