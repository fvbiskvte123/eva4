from services.usuario_service import UserService
from dao.usuario_dao import UserDAO

class UserController:
    def __init__(self, db_path):
        self.dao = UserDAO(db_path)
        self.service = UserService(self.dao)

    def authenticate(self, usuario, contrasena):
        return self.service.authenticate(usuario, contrasena)

    def create_usuario(self, usuario_data):
        return self.service.create_usuario(usuario_data)

    def delete_usuario(self, usuario):
        return self.service.delete_usuario(usuario)

    def list_usuarios(self):
        return self.service.list_usuarios()
