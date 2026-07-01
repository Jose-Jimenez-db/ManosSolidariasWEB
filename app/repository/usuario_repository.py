"""
Este archivo implementa el repositorio de usuarios. Se encarga de realizar
las operaciones de acceso a la base de datos relacionadas con los usuarios,
incluyendo el registro de nuevos usuarios y la consulta de información
utilizada durante el proceso de autenticación del sistema.
"""

from app.config.database import SessionLocal
from app.entity.usuario import UsuarioORM


class UsuarioRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, username, password_hash, rol):
        usuario = UsuarioORM(username=username, password_hash=password_hash, rol=rol)
        self.db.add(usuario)
        self.db.commit()
        return usuario

    def get_by_username(self, username):
        return self.db.query(UsuarioORM).filter_by(username=username).first()
