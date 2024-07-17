from services.tique_service import TiqueService
from dao.tique_dao import TiqueDAO

class TiqueController:
    def __init__(self, db_path):
        self.dao = TiqueDAO(db_path)
        self.service = TiqueService(self.dao)

    def create_tique(self, tique_data):
        return self.service.create_tique(tique_data)

    def list_tiques(self):
        return self.service.list_tiques()

    def update_tique_estado(self, tique_id, nuevo_estado):
        return self.service.update_tique_estado(tique_id, nuevo_estado)

    def delete_tique(self, tique_id):
        return self.service.delete_tique(tique_id)
