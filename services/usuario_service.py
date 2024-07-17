from dao.usuario_dao import UserDAO
from models.usuario import User

class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def authenticate(self, usuario, contrasena):
        user = self.dao.get_usuario(usuario)
        if user and user.contrasena == contrasena:
            return user
        return None

    def create_usuario(self, usuario_data):
        usuario = User(None, **usuario_data)
        self.dao.add_usuario(usuario)
        return usuario

    def delete_usuario(self, usuario):
        return self.dao.delete_usuario(usuario)

    def list_usuarios(self):
        return self.dao.get_all_usuarios()
