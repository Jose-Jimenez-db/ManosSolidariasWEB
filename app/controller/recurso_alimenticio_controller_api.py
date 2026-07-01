"""
Este archivo implementa el controlador de recursos alimenticios del sistema.
Define los endpoints encargados de gestionar las operaciones relacionadas
con los recursos alimenticios, delegando la lógica de negocio al servicio
correspondiente y controlando las respuestas enviadas por la API.
"""

from fastapi import APIRouter, HTTPException, Depends

from app.service.recurso_alimenticio_service import RecursoAlimenticioService
from app.schema.recurso_alimenticio_schema import RecursoAlimenticioSchema
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/recursos", tags=["Recursos Alimenticios"])


@router.post("/", response_model=RecursoAlimenticioSchema)
def create_recurso(
        recurso: RecursoAlimenticioSchema,
        usuario_actual: str = Depends(get_current_user)
):
    service = RecursoAlimenticioService()

    try:
        return service.create_recurso(
            recurso.codigo_recurso,
            recurso.nombre,
            recurso.categoria,
            recurso.unidad_medida,
            recurso.cantidad_disponible,
            recurso.costo_unitario
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[RecursoAlimenticioSchema])
def list_recursos():
    service = RecursoAlimenticioService()

    return service.list_recursos()


@router.get("/{codigo_recurso}", response_model=RecursoAlimenticioSchema)
def get_recurso(codigo_recurso: str):
    service = RecursoAlimenticioService()

    recurso = service.get_recurso(codigo_recurso)

    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    return recurso


@router.put("/{codigo_recurso}", response_model=RecursoAlimenticioSchema)
def update_recurso(
        codigo_recurso: str,
        recurso: RecursoAlimenticioSchema,
        usuario_actual: str = Depends(get_current_user)
):
    service = RecursoAlimenticioService()

    try:
        actualizado = service.update_recurso(
            codigo_recurso,
            recurso.nombre,
            recurso.categoria,
            recurso.unidad_medida,
            recurso.cantidad_disponible,
            recurso.costo_unitario
        )

        if not actualizado:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")

        return actualizado

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{codigo_recurso}")
def delete_recurso(
        codigo_recurso: str,
        usuario_actual: str = Depends(get_current_user)
):
    service = RecursoAlimenticioService()

    eliminado = service.delete_recurso(codigo_recurso)

    if not eliminado:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    return {"message": "Recurso eliminado"}


@router.get("/categoria/{categoria}", response_model=list[RecursoAlimenticioSchema])
def list_by_categoria(categoria: str):
    service = RecursoAlimenticioService()

    return service.list_by_categoria(categoria)
