import sqlite3
from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO

# Ruta a la base de datos
db_path = 'database.db'

# Crear la conexión a la base de datos y el cursor
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear las tablas si no existen
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    usuario TEXT,
                    contrasena TEXT,
                    rol TEXT,
                    activo BOOLEAN)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tiques (
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

# Comprobar si hay algún usuario en la tabla usuarios
cursor.execute('SELECT * FROM usuarios')
users = cursor.fetchall()

# Si no hay usuarios, agregar un usuario administrador por defecto
if not users:
    admin_user = Usuario(None, 'Admin', 'admin', 'admin', 'admin')
    usuario_dao = UsuarioDAO(db_path)
    usuario_dao.add_usuario(admin_user)
    print("Usuario administrador creado: usuario='admin', contraseña='admin'")

# Cerrar la conexión
conn.close()
