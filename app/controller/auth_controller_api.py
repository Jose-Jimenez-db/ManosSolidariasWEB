"""
Este archivo implementa el controlador de autenticación del sistema. Define
los endpoints relacionados con el registro de usuarios, el inicio y cierre
de sesión, así como la verificación del usuario autenticado, delegando la
lógica de negocio al servicio correspondiente.
"""

from fastapi import APIRouter, HTTPException, Header, Depends

from app.service.auth_service import AuthService
from app.schema.auth_schema import LoginSchema, UsuarioRegistroSchema, TokenSchema
from app.auth.security import cerrar_sesion
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/registro")
def registro(usuario: UsuarioRegistroSchema):
    service = AuthService()

    try:
        nuevo = service.registrar_usuario(
            usuario.username,
            usuario.password,
            usuario.rol
        )

        return {
            "message": "Usuario creado",
            "username": nuevo.username
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenSchema)
def login(credenciales: LoginSchema):
    service = AuthService()

    try:
        token, rol = service.login(
            credenciales.username,
            credenciales.password
        )

        return TokenSchema(
            access_token=token,
            rol=rol
        )

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
def logout(authorization: str = Header(...)):
    token = authorization.removeprefix("Bearer ").strip()
    cerrar_sesion(token)

    return {"message": "Sesión cerrada"}


@router.get("/me")
def me(usuario_actual: str = Depends(get_current_user)):
    return {"username": usuario_actual}
