from models.persona import Persona
from utils import seguridad
from utils import validaciones as v


class Administrador(Persona):
    def __init__(self, nombre, rut, direccion, telefono, correo,
                 nivel_acceso, usuario, contrasena, id=None,
                 contrasena_ya_hasheada=False):
        super().__init__(nombre, rut, direccion, telefono, correo, id)
        self.guardar_nivel_acceso(nivel_acceso)
        self.guardar_usuario(usuario)
        self.guardar_contraseña(contrasena, contrasena_ya_hasheada)

    def guardar_nivel_acceso(self, nivel_acceso):
        self.__nivel_acceso = v.validar_nivel_acceso(nivel_acceso)

    def obtener_nivel_acceso(self):
        return self.__nivel_acceso

    def guardar_usuario(self, usuario):
        self.__usuario = v.validar_usuario(usuario)

    def obtener_usuario(self):
        return self.__usuario

    def guardar_contraseña(self, contraseña, ya_hasheada=False):
        if ya_hasheada:
            self.__contraseña = contraseña
        else:
            v.validar_contrasena(contraseña)
            self.__contraseña = seguridad.hashear_contrasena(contraseña)

    def obtener_contraseña(self):
        return self.__contraseña

    def verificar_contraseña(self, contraseña):
        return seguridad.verificar_contrasena(contraseña, self.__contraseña)

    def puede_modificar(self):
        return self.__nivel_acceso == "total"

    nivel_acceso = property(obtener_nivel_acceso, guardar_nivel_acceso)
    usuario = property(obtener_usuario, guardar_usuario)

    def imprimir_persona(self):
        return (super().imprimir_persona() +
                f" | Usuario: {self.__usuario} | Acceso: {self.__nivel_acceso}")

    def imprimir_administrador(self):
        return self.imprimir_persona()
