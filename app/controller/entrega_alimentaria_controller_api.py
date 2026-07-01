"""
Este archivo implementa el controlador de entregas alimentarias del sistema.
Define los endpoints encargados de gestionar las operaciones relacionadas
con las entregas, delegando la lógica de negocio al servicio
correspondiente y controlando las respuestas enviadas por la API.
"""

from fastapi import APIRouter, HTTPException, Depends

from app.service.entrega_alimentaria_service import EntregaAlimentariaService
from app.schema.entrega_alimentaria_schema import (
    EntregaAlimentariaCreateSchema,
    EntregaAlimentariaSchema,
    EntregaAlimentariaUpdateSchema
)
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/entregas", tags=["Entregas Alimentarias"])


@router.post("/", response_model=EntregaAlimentariaSchema)
def create_entrega(
        entrega: EntregaAlimentariaCreateSchema,
        usuario_actual: str = Depends(get_current_user)
):
    service = EntregaAlimentariaService()

    try:
        return service.create_entrega(
            entrega.codigo_entrega,
            entrega.identificacion_beneficiario,
            entrega.codigo_recurso,
            entrega.cantidad_entregada,
            entrega.fecha,
            entrega.responsable_entrega
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[EntregaAlimentariaSchema])
def list_entregas():
    service = EntregaAlimentariaService()

    return service.list_entregas()


@router.get("/{codigo_entrega}", response_model=EntregaAlimentariaSchema)
def get_entrega(codigo_entrega: str):
    service = EntregaAlimentariaService()

    entrega = service.get_entrega(codigo_entrega)

    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")

    return entrega


@router.put("/{codigo_entrega}", response_model=EntregaAlimentariaSchema)
def update_entrega(
        codigo_entrega: str,
        datos: EntregaAlimentariaUpdateSchema,
        usuario_actual: str = Depends(get_current_user)
):
    service = EntregaAlimentariaService()

    try:
        actualizado = service.update_entrega(
            codigo_entrega,
            datos.fecha,
            datos.responsable_entrega
        )

        if not actualizado:
            raise HTTPException(status_code=404, detail="Entrega no encontrada")

        return actualizado

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{codigo_entrega}")
def delete_entrega(
        codigo_entrega: str,
        usuario_actual: str = Depends(get_current_user)
):
    service = EntregaAlimentariaService()

    eliminado = service.delete_entrega(codigo_entrega)

    if not eliminado:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")

    return {"message": "Entrega eliminada y stock restaurado"}
