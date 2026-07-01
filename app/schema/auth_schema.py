"""
Este archivo define los esquemas de validación utilizados en los procesos de
autenticación del sistema. Incluye los modelos necesarios para el inicio de
sesión, el registro de usuarios y la respuesta generada al autenticar un
usuario mediante un token de acceso.
"""

from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class UsuarioRegistroSchema(BaseModel):
    username: str
    password: str
    rol: str = "voluntario"


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str
