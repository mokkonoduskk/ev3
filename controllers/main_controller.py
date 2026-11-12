from controllers.administrador_controller import AdministradorController
from controllers.departamento_controller import DepartamentoController
from controllers.empleado_controller import EmpleadoController
from controllers.proyecto_controller import ProyectoController
from controllers.registro_tiempo_controller import RegistroTiempoController
from controllers.reporte_controller import ReporteController
from views.main_view import MainView


class MainController:
    def __init__(self):
        self.view = MainView()

    def ejecutar(self):
        self.view.mostrar_bienvenida()
        sesion = AdministradorController().autenticar()
        if sesion is None:
            self.view.mostrar_mensaje(
                "Demasiados intentos fallidos. Cerrando el sistema.")
            return

        controladores = {
            1: DepartamentoController(sesion),
            2: EmpleadoController(sesion),
            3: ProyectoController(sesion),
            4: RegistroTiempoController(sesion),
            5: ReporteController(sesion),
            6: AdministradorController(sesion),
        }
        while True:
            opcion = self.view.mostrar_menu()
            if opcion == 0:
                self.view.mostrar_mensaje(
                    "Gracias por usar el sistema de EcoTech.")
                break
            if opcion in controladores:
                controladores[opcion].ejecutar()
            else:
                self.view.mostrar_mensaje(
                    "Opción no válida. Por favor, intente nuevamente.")
