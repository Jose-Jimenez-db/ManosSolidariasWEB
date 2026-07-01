"""
Este archivo define la entidad UsuarioORM, la cual representa la tabla de
usuarios en la base de datos. Contiene la información necesaria para la
autenticación del sistema, incluyendo el nombre de usuario, la contraseña
encriptada y el rol asignado a cada usuario.
"""

from sqlalchemy import Column, String, Integer
from app.config.database import Base


class UsuarioORM(Base):
    __tablename__ = "usuarios_tb"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    rol = Column(String(20), nullable=False, default="voluntario")

    def __repr__(self):
        return f"UsuarioORM(username='{self.username}', rol='{self.rol}')"
