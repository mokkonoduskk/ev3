from utils import validaciones as v


class Empleado:
    def __init__(self, nombre, edad, rut, direccion, telefono, correo,
                 inicio_contrato, salario, id_empleado=None,
                 id_departamento=None):
        self.guardar_id_empleado(id_empleado)
        self.guardar_nombre(nombre)
        self.guardar_edad(edad)
        self.guardar_rut(rut)
        self.guardar_direccion(direccion)
        self.guardar_telefono(telefono)
        self.guardar_correo(correo)
        self.guardar_inicio_contrato(inicio_contrato)
        self.guardar_salario(salario)
        self.guardar_id_departamento(id_departamento)

    def guardar_id_empleado(self, id_empleado):
        self.__id_empleado = v.validar_id(id_empleado)

    def obtener_id_empleado(self):
        return self.__id_empleado

    def guardar_nombre(self, nombre):
        self.__nombre = v.validar_texto(nombre, "El nombre")

    def obtener_nombre(self):
        return self.__nombre

    def guardar_edad(self, edad):
        self.__edad = v.validar_entero(edad, "La edad", 18, 99)

    def obtener_edad(self):
        return self.__edad

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

    def obtener_correo_electronico(self):
        return self.__correo

    def guardar_inicio_contrato(self, inicio_contrato):
        self.__inicio_contrato = v.validar_fecha(
            inicio_contrato, "El inicio de contrato")

    def obtener_inicio_contrato(self):
        return self.__inicio_contrato

    def guardar_salario(self, salario):
        self.__salario = v.validar_decimal(salario, "El salario", minimo=0)

    def obtener_salario(self):
        return self.__salario

    def guardar_id_departamento(self, id_departamento):
        self.__id_departamento = v.validar_id(id_departamento)

    def obtener_id_departamento(self):
        return self.__id_departamento

    id_empleado = property(obtener_id_empleado, guardar_id_empleado)
    nombre = property(obtener_nombre, guardar_nombre)
    edad = property(obtener_edad, guardar_edad)
    rut = property(obtener_rut, guardar_rut)
    direccion = property(obtener_direccion, guardar_direccion)
    telefono = property(obtener_telefono, guardar_telefono)
    correo = property(obtener_correo_electronico, guardar_correo)
    inicio_contrato = property(obtener_inicio_contrato, guardar_inicio_contrato)
    salario = property(obtener_salario, guardar_salario)
    id_departamento = property(obtener_id_departamento, guardar_id_departamento)

    def imprimir_empleado(self, mostrar_salario=False):
        """El salario es sensible: solo se muestra si se pide explicitamente."""
        salario = f"${self.__salario:,.0f}" if mostrar_salario else "*****"
        return (f"[{self.__id_empleado}] {self.__nombre} ({self.__edad} anios) | "
                f"RUT: {self.__rut} | Tel: {self.__telefono} | "
                f"Correo: {self.__correo} | Contrato desde: "
                f"{self.__inicio_contrato} | Salario: {salario} | "
                f"Depto: {self.__id_departamento or 'sin asignar'}")

    def __str__(self):
        return self.imprimir_empleado()
