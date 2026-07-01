"""
Este archivo implementa las funciones relacionadas con la seguridad y la
autenticación del sistema. Se encarga de generar y verificar contraseñas
encriptadas, administrar las sesiones activas mediante tokens y permitir
el cierre de sesión de los usuarios autenticados.
"""

import hashlib
import secrets


_active_sessions: dict[str, str] = {}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def crear_sesion(username: str) -> str:
    token = secrets.token_urlsafe(32)
    _active_sessions[token] = username
    return token


def obtener_usuario_de_token(token: str):
    return _active_sessions.get(token)


def cerrar_sesion(token: str) -> None:
    _active_sessions.pop(token, None)
