import sqlite3
from models.usuario import User

class UserDAO:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre TEXT,
                                usuario TEXT UNIQUE,
                                contrasena TEXT,
                                rol TEXT)''')
        self.conn.commit()

    def add_usuario(self, usuario):
        self.cursor.execute('''INSERT INTO usuarios (nombre, usuario, contrasena, rol)
                               VALUES (?, ?, ?, ?)''', 
                               (usuario.nombre, usuario.usuario, usuario.contrasena, usuario.rol))
        self.conn.commit()

    def get_usuario(self, usuario):
        self.cursor.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,))
        row = self.cursor.fetchone()
        if row:
            return User(row['id'], row['nombre'], row['usuario'], row['contrasena'], row['rol'])
        return None

    def delete_usuario(self, usuario):
        self.cursor.execute('DELETE FROM usuarios WHERE usuario = ?', (usuario,))
        self.conn.commit()

    def get_all_usuarios(self):
        self.cursor.execute('SELECT * FROM usuarios')
        rows = self.cursor.fetchall()
        return [User(row['id'], row['nombre'], row['usuario'], row['contrasena'], row['rol']) for row in rows]
