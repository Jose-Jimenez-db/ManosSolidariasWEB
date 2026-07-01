"""
Este archivo implementa el controlador de beneficiarios del sistema. Define
los endpoints encargados de gestionar las operaciones relacionadas con los
beneficiarios, delegando la lógica de negocio al servicio correspondiente y
controlando las respuestas enviadas por la API.
"""

from fastapi import APIRouter, HTTPException, Depends

from app.service.beneficiario_service import BeneficiarioService
from app.schema.beneficiario_schema import BeneficiarioSchema
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/beneficiarios", tags=["Beneficiarios"])


@router.post("/", response_model=BeneficiarioSchema)
def create_beneficiario(
        beneficiario: BeneficiarioSchema,
        usuario_actual: str = Depends(get_current_user)
):
    service = BeneficiarioService()

    try:
        return service.create_beneficiario(
            beneficiario.identificacion,
            beneficiario.nombre_completo,
            beneficiario.comunidad,
            beneficiario.integrantes_hogar,
            beneficiario.prioridad_social
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[BeneficiarioSchema])
def list_beneficiarios():
    service = BeneficiarioService()

    return service.list_beneficiarios()


@router.get("/{identificacion}", response_model=BeneficiarioSchema)
def get_beneficiario(identificacion: str):
    service = BeneficiarioService()

    beneficiario = service.get_beneficiario(identificacion)

    if not beneficiario:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")

    return beneficiario


@router.put("/{identificacion}", response_model=BeneficiarioSchema)
def update_beneficiario(
        identificacion: str,
        beneficiario: BeneficiarioSchema,
        usuario_actual: str = Depends(get_current_user)
):
    service = BeneficiarioService()

    try:
        actualizado = service.update_beneficiario(
            identificacion,
            beneficiario.nombre_completo,
            beneficiario.comunidad,
            beneficiario.integrantes_hogar,
            beneficiario.prioridad_social
        )

        if not actualizado:
            raise HTTPException(status_code=404, detail="Beneficiario no encontrado")

        return actualizado

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{identificacion}")
def delete_beneficiario(
        identificacion: str,
        usuario_actual: str = Depends(get_current_user)
):
    service = BeneficiarioService()

    eliminado = service.delete_beneficiario(identificacion)

    if not eliminado:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")

    return {"message": "Beneficiario eliminado"}
