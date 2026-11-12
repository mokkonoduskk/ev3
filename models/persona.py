from utils import validaciones as v


class Persona:
    def __init__(self, nombre, rut, direccion, telefono, correo, id=None):
        self.guardar_id(id)
        self.guardar_nombre(nombre)
        self.guardar_rut(rut)
        self.guardar_direccion(direccion)
        self.guardar_telefono(telefono)
        self.guardar_correo(correo)

    def guardar_id(self, id):
        self.__id = v.validar_id(id)

    def obtener_id(self):
        return self.__id

    def guardar_nombre(self, nombre):
        self.__nombre = v.validar_texto(nombre, "El nombre")

    def obtener_nombre(self):
        return self.__nombre

    def guardar_rut(self, rut):
        self.__rut = v.validar_rut(rut)

    def obtener_rut(self):
        return self.__rut

    def guardar_direccion(self, direccion):
        self.__direccion = v.validar_texto(direccion, "La direccion", 5, 150)

    def obtener_direccion(self):
        return self.__direccion

    def guardar_telefono(self, telefono):
        self.__telefono = v.validar_telefono(telefono)

    def obtener_telefono(self):
        return self.__telefono

    def guardar_correo(self, correo):
        self.__correo = v.validar_correo(correo)

    def obtener_correo(self):
        return self.__correo

    id = property(obtener_id, guardar_id)
    nombre = property(obtener_nombre, guardar_nombre)
    rut = property(obtener_rut, guardar_rut)
    direccion = property(obtener_direccion, guardar_direccion)
    telefono = property(obtener_telefono, guardar_telefono)
    correo = property(obtener_correo, guardar_correo)

    def imprimir_persona(self):
        return (f"[{self.__id}] {self.__nombre} | RUT: {self.__rut} | "
                f"Dir: {self.__direccion} | Tel: {self.__telefono} | "
                f"Correo: {self.__correo}")

    def __str__(self):
        return self.imprimir_persona()
