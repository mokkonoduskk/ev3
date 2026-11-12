from models.empleado import Empleado
from utils import validaciones as v
from utils.excepciones import ValidacionError


class Proyecto:
    def __init__(self, nombre, descripcion, fecha_inicio, id=None,
                 ciudad="Santiago", pais="CL", moneda="CLP"):
        self.guardar_id(id)
        self.guardar_nombre(nombre)
        self.guardar_descripcion(descripcion)
        self.guardar_fecha_inicio(fecha_inicio)
        self.guardar_ciudad(ciudad)
        self.guardar_pais(pais)
        self.guardar_moneda(moneda)
        self.__empleados = []

    def guardar_id(self, id):
        self.__id = v.validar_id(id)

    def obtener_id(self):
        return self.__id

    def guardar_nombre(self, nombre):
        self.__nombre = v.validar_texto(nombre, "El nombre del proyecto")

    def obtener_nombre(self):
        return self.__nombre

    def guardar_descripcion(self, descripcion):
        self.__descripcion = v.validar_texto(
            descripcion, "La descripcion", 5, 300)

    def obtener_descripcion(self):
        return self.__descripcion

    def guardar_fecha_inicio(self, fecha_inicio):
        self.__fecha_inicio = v.validar_fecha(
            fecha_inicio, "La fecha de inicio")

    def obtener_fecha_inicio(self):
        return self.__fecha_inicio

    def guardar_ciudad(self, ciudad):
        self.__ciudad = v.validar_ciudad(ciudad)

    def obtener_ciudad(self):
        return self.__ciudad

    def guardar_pais(self, pais):
        self.__pais = v.validar_codigo_pais(pais)

    def obtener_pais(self):
        return self.__pais

    def guardar_moneda(self, moneda):
        self.__moneda = v.validar_moneda(moneda)

    def obtener_moneda(self):
        return self.__moneda

    def asignar_empleado(self, empleado):
        if not isinstance(empleado, Empleado):
            raise ValidacionError("Solo se pueden asignar objetos Empleado.")
        self.__empleados.append(empleado)

    def obtener_empleados(self):
        return list(self.__empleados)

    id = property(obtener_id, guardar_id)
    nombre = property(obtener_nombre, guardar_nombre)
    descripcion = property(obtener_descripcion, guardar_descripcion)
    fecha_inicio = property(obtener_fecha_inicio, guardar_fecha_inicio)
    ciudad = property(obtener_ciudad, guardar_ciudad)
    pais = property(obtener_pais, guardar_pais)
    moneda = property(obtener_moneda, guardar_moneda)

    def imprimir_proyecto(self):
        return (f"[{self.__id}] {self.__nombre} | Inicio: {self.__fecha_inicio}"
                f" | {self.__descripcion} | Ubicacion: {self.__ciudad}, "
                f"{self.__pais} | Moneda: {self.__moneda} | "
                f"Empleados: {len(self.__empleados)}")

    def __str__(self):
        return self.imprimir_proyecto()
