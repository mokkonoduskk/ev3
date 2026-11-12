from controllers.base_controller import BaseController
from models.registro_tiempo_dao import RegistroTiempoDAO
from views.reporte_view import ReporteView


class ReporteController(BaseController):
    def __init__(self, sesion):
        super().__init__(ReporteView(), sesion)

    def acciones(self):
        return {1: (self.horas_por_proyecto, False),
                2: (self.horas_por_empleado, False)}

    def horas_por_proyecto(self):
        self.view.mostrar_reporte("Horas por proyecto",
                                  RegistroTiempoDAO.horas_por_proyecto())

    def horas_por_empleado(self):
        self.view.mostrar_reporte("Horas por empleado",
                                  RegistroTiempoDAO.horas_por_empleado())
