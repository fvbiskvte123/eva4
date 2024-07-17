from datetime import datetime

class Tique:
    def __init__(self, id, nombre_cliente, rut_cliente, telefono, correo, tipo_tique, criticidad, detalle_servicio, detalle_problema, area, estado, creado_por, creado_en=None, asignado_a=None, cerrado_por=None, cerrado_en=None):
        self.id = id
        self.nombre_cliente = nombre_cliente
        self.rut_cliente = rut_cliente
        self.telefono = telefono
        self.correo = correo
        self.tipo_tique = tipo_tique
        self.criticidad = criticidad
        self.detalle_servicio = detalle_servicio
        self.detalle_problema = detalle_problema
        self.area = area
        self.estado = estado
        self.creado_por = creado_por
        self.creado_en = creado_en or datetime.now()
        self.asignado_a = asignado_a
        self.cerrado_por = cerrado_por
        self.cerrado_en = cerrado_en
