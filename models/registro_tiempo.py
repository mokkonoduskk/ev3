from utils import validaciones as v


class RegistroTiempo:
    def __init__(self, fecha, horas_trabajadas, desc_tareas,
                 id_empleado, id_proyecto, id=None):
        self.guardar_id(id)
        self.guardar_fecha(fecha)
        self.guardar_horas_trabajadas(horas_trabajadas)
        self.guardar_desc_tareas(desc_tareas)
        self.guardar_id_empleado(id_empleado)
        self.guardar_id_proyecto(id_proyecto)

    def guardar_id(self, id):
        self.__id = v.validar_id(id)

    def obtener_id(self):
        return self.__id

    def guardar_fecha(self, fecha):
        self.__fecha = v.validar_fecha(fecha, "La fecha", permitir_futuro=False)

    def obtener_fecha(self):
        return self.__fecha

    def guardar_horas_trabajadas(self, horas_trabajadas):
        self.__horas_trabajadas = v.validar_entero(
            horas_trabajadas, "Las horas trabajadas", 1, 24)

    def obtener_horas_trabajadas(self):
        return self.__horas_trabajadas

    def guardar_desc_tareas(self, desc_tareas):
        self.__desc_tareas = v.validar_texto(
            desc_tareas, "La descripcion de tareas", 5, 300)

    def obtener_desc_tareas(self):
        return self.__desc_tareas

    def guardar_id_empleado(self, id_empleado):
        self.__id_empleado = v.validar_entero(id_empleado, "ID de empleado", 1)

    def obtener_id_empleado(self):
        return self.__id_empleado

    def guardar_id_proyecto(self, id_proyecto):
        self.__id_proyecto = v.validar_entero(id_proyecto, "ID de proyecto", 1)

    def obtener_id_proyecto(self):
        return self.__id_proyecto

    id = property(obtener_id, guardar_id)
    fecha = property(obtener_fecha, guardar_fecha)
    horas_trabajadas = property(obtener_horas_trabajadas,
                                guardar_horas_trabajadas)
    desc_tareas = property(obtener_desc_tareas, guardar_desc_tareas)
    id_empleado = property(obtener_id_empleado, guardar_id_empleado)
    id_proyecto = property(obtener_id_proyecto, guardar_id_proyecto)

    def imprimir_registro_de_tiempo(self):
        return (f"[{self.__id}] {self.__fecha} | Empleado {self.__id_empleado}"
                f" | Proyecto {self.__id_proyecto} | "
                f"{self.__horas_trabajadas} h | {self.__desc_tareas}")

    def __str__(self):
        return self.imprimir_registro_de_tiempo()
