"""
Este archivo define las dependencias utilizadas por FastAPI para validar la
autenticación de los usuarios. Se encarga de verificar la existencia y
validez del token de acceso antes de permitir el uso de los servicios
protegidos del sistema.
"""

from fastapi import Header, HTTPException
from app.auth.security import obtener_usuario_de_token


def get_current_user(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    token = authorization.removeprefix("Bearer ").strip()
    username = obtener_usuario_de_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")

    return username
