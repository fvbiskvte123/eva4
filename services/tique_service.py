from dao.tique_dao import TiqueDAO
from models.tique import Tique

class TiqueService:
    def __init__(self, dao: TiqueDAO):
        self.dao = dao

    def create_tique(self, tique_data):
        tique = Tique(None, **tique_data)
        self.dao.add_tique(tique)
        return tique

    def list_tiques(self):
        return self.dao.get_all_tiques()

    def update_tique_estado(self, tique_id, nuevo_estado):
        return self.dao.update_tique_estado(tique_id, nuevo_estado)

    def delete_tique(self, tique_id):
        return self.dao.delete_tique(tique_id)
