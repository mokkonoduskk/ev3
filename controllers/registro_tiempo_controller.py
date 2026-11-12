from controllers.base_controller import BaseController
from models.registro_tiempo import RegistroTiempo
from models.registro_tiempo_dao import RegistroTiempoDAO
from views.registro_tiempo_view import RegistroTiempoView


class RegistroTiempoController(BaseController):
    def __init__(self, sesion):
        super().__init__(RegistroTiempoView(), sesion)

    def acciones(self):
        return {1: (self.agregar_registro, True),
                2: (self.editar_registro, True),
                3: (self.eliminar_registro, True),
                4: (self.imprimir_registro, False),
                5: (self.imprimir_registros, False),
                6: (self.imprimir_registros_empleado, False)}

    def agregar_registro(self):
        datos = self.view.formulario_nuevo_registro()
        registro = RegistroTiempo(**datos)
        RegistroTiempoDAO.crear(registro)
        self.view.mostrar_mensaje(
            f"Registro agregado exitosamente con ID {registro.id}.")

    def editar_registro(self):
        registro = RegistroTiempoDAO.obtener_por_id(self.view.solicitar_id())
        if not registro:
            self.view.mostrar_mensaje("Registro no encontrado.")
            return
        datos = self.view.formulario_editar_registro(registro)
        registro.fecha = datos["fecha"]
        registro.horas_trabajadas = datos["horas_trabajadas"]
        registro.desc_tareas = datos["desc_tareas"]
        RegistroTiempoDAO.actualizar(registro)
        self.view.mostrar_mensaje("Registro actualizado exitosamente.")

    def eliminar_registro(self):
        id_registro = self.view.solicitar_id()
        if not RegistroTiempoDAO.existe(id_registro):
            self.view.mostrar_mensaje("Registro no encontrado.")
            return
        if self.view.confirmar_eliminacion():
            RegistroTiempoDAO.eliminar(id_registro)
            self.view.mostrar_mensaje("Registro eliminado exitosamente.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")

    def imprimir_registro(self):
        registro = RegistroTiempoDAO.obtener_por_id(self.view.solicitar_id())
        if registro:
            self.view.mostrar_registro(registro)
        else:
            self.view.mostrar_mensaje("Registro no encontrado.")

    def imprimir_registros(self):
        self.view.mostrar_lista_registros(RegistroTiempoDAO.obtener_todos())

    def imprimir_registros_empleado(self):
        id_empleado = self.view.solicitar_id("Ingrese el ID del empleado")
        self.view.mostrar_lista_registros(
            RegistroTiempoDAO.obtener_por_empleado(id_empleado))
