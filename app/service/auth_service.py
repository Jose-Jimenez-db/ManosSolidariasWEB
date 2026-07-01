"""
Este archivo implementa el servicio de autenticación del sistema. Se encarga
de gestionar el registro de usuarios, validar las credenciales durante el
inicio de sesión, crear las sesiones de acceso y garantizar la existencia
de un usuario administrador por defecto.
"""

from app.repository.usuario_repository import UsuarioRepository
from app.auth.security import hash_password, verify_password, crear_sesion


class AuthService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def registrar_usuario(self, username, password, rol="voluntario"):
        if username.strip() == "":
            raise ValueError("El usuario no puede estar vacío.")
        if len(password) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres.")
        if self.repo.get_by_username(username):
            raise ValueError("El usuario ya existe.")

        return self.repo.create(username.strip(), hash_password(password), rol)

    def login(self, username, password):
        usuario = self.repo.get_by_username(username)
        if not usuario or not verify_password(password, usuario.password_hash):
            raise ValueError("Usuario o contraseña incorrectos.")

        token = crear_sesion(usuario.username)
        return token, usuario.rol

    def asegurar_admin_por_defecto(self):
        if not self.repo.get_by_username("admin"):
            self.repo.create("admin", hash_password("admin123"), "admin")
