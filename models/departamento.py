from models.empleado import Empleado
from utils import validaciones as v
from utils.excepciones import ValidacionError


class Departamento:
    def __init__(self, nombre, gerente_asociado, id=None):
        self.guardar_id(id)
        self.guardar_nombre(nombre)
        self.guardar_gerente_asociado(gerente_asociado)
        self.__empleados = []

    def guardar_id(self, id):
        self.__id = v.validar_id(id)

    def obtener_id(self):
        return self.__id

    def guardar_nombre(self, nombre):
        self.__nombre = v.validar_texto(nombre, "El nombre del departamento")

    def obtener_nombre(self):
        return self.__nombre

    def guardar_gerente_asociado(self, gerente_asociado):
        self.__gerente_asociado = v.validar_texto(
            gerente_asociado, "El gerente asociado")

    def obtener_gerente_asociado(self):
        return self.__gerente_asociado

    def agregar_empleado(self, empleado):
        if not isinstance(empleado, Empleado):
            raise ValidacionError("Solo se pueden agregar objetos Empleado.")
        self.__empleados.append(empleado)

    def obtener_empleados(self):
        return list(self.__empleados)

    id = property(obtener_id, guardar_id)
    nombre = property(obtener_nombre, guardar_nombre)
    gerente_asociado = property(obtener_gerente_asociado,
                                guardar_gerente_asociado)

    def imprimir_departamento(self):
        return (f"[{self.__id}] {self.__nombre} | Gerente: "
                f"{self.__gerente_asociado} | Empleados: {len(self.__empleados)}")

    def __str__(self):
        return self.imprimir_departamento()
