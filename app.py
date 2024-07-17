import curses
from controllers.tique_controller import TiqueController
from controllers.user_controller import UserController
from config import Config

def login(stdscr, user_controller):
    stdscr.clear()
    stdscr.addstr(0, 0, "Sistema de Gestión de Tiques - Inicio de Sesión")
    stdscr.addstr(1, 0, "Usuario: ")
    stdscr.refresh()
    curses.echo()
    usuario = stdscr.getstr(1, 9, 20).decode('utf-8')
    stdscr.addstr(2, 0, "Contraseña: ")
    curses.noecho()
    contrasena = stdscr.getstr(2, 12, 20).decode('utf-8')
    curses.echo()
    user = user_controller.authenticate(usuario, contrasena)
    if user:
        stdscr.addstr(4, 0, f"Bienvenido {user.nombre}")
        stdscr.refresh()
        stdscr.getch()
        return user
    else:
        stdscr.addstr(4, 0, "Usuario o contraseña incorrectos")
        stdscr.refresh()
        stdscr.getch()
        return None

def get_input(stdscr, prompt, y, x, echo=True):
    max_y, max_x = stdscr.getmaxyx()
    if y >= max_y or x + len(prompt) >= max_x:
        raise ValueError("Posición fuera de los límites de la ventana")
    stdscr.addstr(y, x, prompt)
    if echo:
        curses.echo()
    else:
        curses.noecho()
    input_str = stdscr.getstr(y, x + len(prompt), 30).decode('utf-8').strip()
    curses.echo()
    return input_str

def select_tique_type(stdscr):
    stdscr.addstr(5, 0, "Seleccione Tipo de Tique:")
    tique_types = ["1. Felicitación", "2. Consulta", "3. Reclamo", "4. Problema"]
    for idx, tique_type in enumerate(tique_types, start=1):
        stdscr.addstr(5 + idx, 0, tique_type)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('1'):
            return "Felicitación"
        elif key == ord('2'):
            return "Consulta"
        elif key == ord('3'):
            return "Reclamo"
        elif key == ord('4'):
            return "Problema"

def create_tique(stdscr, user, tique_controller):
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        current_y = 0

        def safe_addstr(y, x, text):
            if y < max_y and x + len(text) < max_x:
                stdscr.addstr(y, x, text)
        
        safe_addstr(current_y, 0, "Crear Tique")
        current_y += 1

        nombre_cliente = get_input(stdscr, "Nombre Cliente: ", current_y, 0)
        if not nombre_cliente:
            safe_addstr(current_y + 1, 0, "El nombre del cliente no puede estar en blanco.")
            stdscr.refresh()
            stdscr.getch()
            continue
        current_y += 1
        
        rut_cliente = get_input(stdscr, "RUT Cliente: ", current_y, 0)
        if not rut_cliente:
            safe_addstr(current_y + 1, 0, "El RUT del cliente no puede estar en blanco.")
            stdscr.refresh()
            stdscr.getch()
            continue
        current_y += 1

        telefono = get_input(stdscr, "Teléfono: ", current_y, 0)
        if not telefono:
            safe_addstr(current_y + 1, 0, "El teléfono no puede estar en blanco.")
            stdscr.refresh()
            stdscr.getch()
            continue
        current_y += 1

        correo = get_input(stdscr, "Correo: ", current_y, 0)
        if not correo:
            safe_addstr(current_y + 1, 0, "El correo no puede estar en blanco.")
            stdscr.refresh()
            stdscr.getch()
            continue
        current_y += 1

        tipo_tique = select_tique_type(stdscr)
        current_y += 1

        criticidad = get_input(stdscr, "Criticidad: ", current_y, 0)
        if not criticidad:
            safe_addstr(current_y + 1, 0, "La criticidad no puede estar en blanco.")
            stdscr.refresh()
            stdscr.getch()
            continue
        current_y += 1

        detalle_servicio = get_input(stdscr, "Detalle Servicio: ", current_y, 0)
        if not detalle_servicio:
            safe_addstr(current_y + 1, 0, "El detalle del servicio no puede estar en blanco.")
            stdscr.refresh()
            stdscr.getch()
            continue
        current_y += 1

        detalle_problema = get_input(stdscr, "Detalle Problema: ", current_y, 0)
        if not detalle_problema:
            safe_addstr(current_y + 1, 0, "El detalle del problema no puede estar en blanco.")
            stdscr.refresh()
            stdscr.getch()
            continue
        current_y += 1

        area = get_input(stdscr, "Área: ", current_y, 0)
        if not area:
            safe_addstr(current_y + 1, 0, "El área no puede estar en blanco.")
            stdscr.refresh()
            stdscr.getch()
            continue
        current_y += 1

        creado_por = user.usuario  # Usuario autenticado

        tique_data = {
            "nombre_cliente": nombre_cliente,
            "rut_cliente": rut_cliente,
            "telefono": telefono,
            "correo": correo,
            "tipo_tique": tipo_tique,
            "criticidad": criticidad,
            "detalle_servicio": detalle_servicio,
            "detalle_problema": detalle_problema,
            "area": area,
            "estado": "Nuevo",  # Estado inicial fijo
            "creado_por": creado_por
        }

        safe_addstr(current_y, 0, "Previsualización del Tique:")
        current_y += 1
        for key, value in tique_data.items():
            if current_y >= max_y - 1:
                break
            safe_addstr(current_y, 0, f"{key}: {value[:60]}")
            current_y += 1
        stdscr.refresh()
        stdscr.getch()

        tique_controller.create_tique(tique_data)
        safe_addstr(current_y + 1, 0, "Tique creado exitosamente!")
        safe_addstr(current_y + 2, 0, "Presiona 'c' para crear otro tique o 'q' para volver al menú principal.")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('c'):
            continue

def edit_tique(stdscr, tique_controller):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    current_y = 0

    def safe_addstr(y, x, text):
        if y < max_y and x + len(text) < max_x:
            stdscr.addstr(y, x, text)
    
    safe_addstr(current_y, 0, "Editar Tique")
    current_y += 1
    safe_addstr(current_y, 0, "ID del Tique: ")
    tique_id = stdscr.getstr(current_y, 14, 10).decode('utf-8')
    
    safe_addstr(current_y + 1, 0, "1. Cambiar estado")
    safe_addstr(current_y + 2, 0, "2. Eliminar tique")
    safe_addstr(current_y + 3, 0, "Seleccione una opción: ")
    stdscr.refresh()
    
    key = stdscr.getch()
    
    if key == ord('1'):
        safe_addstr(current_y + 4, 0, "Nuevo Estado (En Progreso/Resuelto/Cerrado): ")
        nuevo_estado = stdscr.getstr(current_y + 4, 40, 20).decode('utf-8')
        tique_controller.update_tique_estado(tique_id, nuevo_estado)
        safe_addstr(current_y + 6, 0, "Tique actualizado exitosamente!")
        stdscr.refresh()
        stdscr.getch()
    elif key == ord('2'):
        tique_controller.delete_tique(tique_id)
        safe_addstr(current_y + 4, 0, "Tique eliminado exitosamente!")
        stdscr.refresh()
        stdscr.getch()

def delete_user(stdscr, user_controller):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    current_y = 0

    def safe_addstr(y, x, text):
        if y < max_y and x + len(text) < max_x:
            stdscr.addstr(y, x, text)
    
    safe_addstr(current_y, 0, "Eliminar Usuario")
    current_y += 1
    safe_addstr(current_y, 0, "Usuario: ")
    usuario = stdscr.getstr(current_y, 9, 20).decode('utf-8')
    user_controller.delete_usuario(usuario)
    safe_addstr(current_y + 2, 0, "Usuario eliminado exitosamente!")
    stdscr.refresh()
    stdscr.getch()

def list_tiques(stdscr, tique_controller):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    current_y = 0

    def safe_addstr(y, x, text):
        if y < max_y and x + len(text) < max_x:
            stdscr.addstr(y, x, text)

    safe_addstr(current_y, 0, "Listar Tiques")
    current_y += 1
    
    # Encabezados de la tabla
    headers = ["ID", "Ejecutivo", "Fecha Creación", "Tipo Tique", "Criticidad", "Área", "Estado"]
    header_str = "{:<5} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(*headers)
    safe_addstr(current_y, 0, header_str)
    current_y += 1
    safe_addstr(current_y, 0, "-" * len(header_str))
    current_y += 1
    
    tiques = tique_controller.list_tiques()
    for tique in tiques:
        if current_y >= max_y - 1:
            break
        # Filas de la tabla
        tique_str = "{:<5} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
            tique.id, tique.creado_por, str(tique.creado_en), tique.tipo_tique, tique.criticidad, tique.area, tique.estado[:10])
        safe_addstr(current_y, 0, tique_str)
        current_y += 1

    stdscr.refresh()
    stdscr.getch()

def list_users(stdscr, user_controller):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    current_y = 0

    def safe_addstr(y, x, text):
        if y < max_y and x + len(text) < max_x:
            stdscr.addstr(y, x, text)
    
    safe_addstr(current_y, 0, "Listar Usuarios")
    current_y += 1
    
    # Encabezados de la tabla
    headers = ["ID", "Nombre", "Usuario", "Rol"]
    header_str = "{:<5} {:<15} {:<15} {:<10}".format(*headers)
    safe_addstr(current_y, 0, header_str)
    current_y += 1
    safe_addstr(current_y, 0, "-" * len(header_str))
    current_y += 1
    
    usuarios = user_controller.list_usuarios()
    for usuario in usuarios:
        if current_y >= max_y - 1:
            break
        # Filas de la tabla
        usuario_str = "{:<5} {:<15} {:<15} {:<10}".format(
            usuario.id, usuario.nombre, usuario.usuario, usuario.rol)
        safe_addstr(current_y, 0, usuario_str)
        current_y += 1

    stdscr.refresh()
    stdscr.getch()

def main_menu(stdscr, user, user_controller, tique_controller):
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        current_y = 0

        def safe_addstr(y, x, text):
            if y < max_y and x + len(text) < max_x:
                stdscr.addstr(y, x, text)

        safe_addstr(current_y, 0, "Sistema de Gestión de Tiques")
        current_y += 1

        if user.rol == 'admin' or user.rol == 'ejecutivo':
            safe_addstr(current_y, 0, "1. Crear Usuario")
            safe_addstr(current_y + 1, 0, "2. Eliminar Usuario")
            safe_addstr(current_y + 2, 0, "3. Listar Usuarios")
            safe_addstr(current_y + 3, 0, "4. Crear Tique")
            safe_addstr(current_y + 4, 0, "5. Editar Tique")
            safe_addstr(current_y + 5, 0, "6. Listar Tiques")
            safe_addstr(current_y + 6, 0, "7. Salir")
        else:
            safe_addstr(current_y, 0, "1. Crear Tique")
            safe_addstr(current_y + 1, 0, "2. Salir")

        stdscr.refresh()

        key = stdscr.getch()
        
        if (user.rol == 'admin' or user.rol == 'ejecutivo') and key == ord('1'):
            stdscr.clear()
            stdscr.addstr(0, 0, "Crear Usuario")
            stdscr.addstr(1, 0, "Nombre: ")
            nombre = stdscr.getstr(1, 8, 20).decode('utf-8')
            stdscr.addstr(2, 0, "Usuario: ")
            usuario = stdscr.getstr(2, 9, 20).decode('utf-8')
            stdscr.addstr(3, 0, "Contraseña: ")
            curses.noecho()
            contrasena = stdscr.getstr(3, 12, 20).decode('utf-8')
            curses.echo()
            stdscr.addstr(4, 0, "Rol (admin/user/ejecutivo): ")
            rol = stdscr.getstr(4, 25, 10).decode('utf-8')
            user_controller.create_usuario({"nombre": nombre, "usuario": usuario, "contrasena": contrasena, "rol": rol})
            stdscr.addstr(6, 0, "Usuario creado exitosamente!")
            stdscr.refresh()
            stdscr.getch()
        
        elif (user.rol == 'admin' or user.rol == 'ejecutivo') and key == ord('2'):
            delete_user(stdscr, user_controller)
        
        elif (user.rol == 'admin' or user.rol == 'ejecutivo') and key == ord('3'):
            list_users(stdscr, user_controller)
        
        elif key == ord('1') and user.rol == 'user':
            create_tique(stdscr, user, tique_controller)

        elif (user.rol == 'admin' or user.rol == 'ejecutivo') and key == ord('4'):
            create_tique(stdscr, user, tique_controller)
        
        elif (user.rol == 'admin' or user.rol == 'ejecutivo') and key == ord('5'):
            edit_tique(stdscr, tique_controller)
        
        elif (user.rol == 'admin' or user.rol == 'ejecutivo') and key == ord('6'):
            list_tiques(stdscr, tique_controller)
        
        elif (user.rol == 'admin' or user.rol == 'ejecutivo') and key == ord('7') or (user.rol == 'user' and key == ord('2')):
            return False

def main(stdscr):
    user_controller = UserController(Config.DATABASE_URI)
    tique_controller = TiqueController(Config.DATABASE_URI)

    while True:
        user = None
        while not user:
            user = login(stdscr, user_controller)
        
        if not main_menu(stdscr, user, user_controller, tique_controller):
            continue

if __name__ == '__main__':
    curses.wrapper(main)
