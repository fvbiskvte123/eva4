import sqlite3
from models.tique import Tique

class TiqueDAO:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tiques (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre_cliente TEXT,
                                rut_cliente TEXT,
                                telefono TEXT,
                                correo TEXT,
                                tipo_tique TEXT,
                                criticidad TEXT,
                                detalle_servicio TEXT,
                                detalle_problema TEXT,
                                area TEXT,
                                estado TEXT,
                                creado_por TEXT,
                                creado_en TEXT,
                                asignado_a TEXT,
                                cerrado_por TEXT,
                                cerrado_en TEXT)''')
        self.conn.commit()

    def add_tique(self, tique):
        self.cursor.execute('''INSERT INTO tiques (nombre_cliente, rut_cliente, telefono, correo, tipo_tique, criticidad, detalle_servicio, detalle_problema, area, estado, creado_por, creado_en, asignado_a, cerrado_por, cerrado_en)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, ?, ?)''', 
                               (tique.nombre_cliente, tique.rut_cliente, tique.telefono, tique.correo, tique.tipo_tique, tique.criticidad, tique.detalle_servicio, tique.detalle_problema, tique.area, tique.estado, tique.creado_por, None, None, None))
        self.conn.commit()

    def get_all_tiques(self):
        self.cursor.execute('SELECT * FROM tiques')
        rows = self.cursor.fetchall()
        return [Tique(**row) for row in rows]

    def update_tique_estado(self, tique_id, nuevo_estado):
        self.cursor.execute('UPDATE tiques SET estado = ? WHERE id = ?', (nuevo_estado, tique_id))
        self.conn.commit()

    def delete_tique(self, tique_id):
        self.cursor.execute('DELETE FROM tiques WHERE id = ?', (tique_id,))
        self.conn.commit()
