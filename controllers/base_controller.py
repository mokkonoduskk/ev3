from utils.excepciones import ERRORES_CONTROLADOS


class BaseController:
    def __init__(self, view, sesion):
        self.view = view
        self.sesion = sesion

    def acciones(self):
        raise NotImplementedError

    def ejecutar(self):
        acciones = self.acciones()
        while True:
            opcion = self.view.mostrar_menu()
            if opcion == 0:
                self.view.mostrar_mensaje("Volviendo al menú principal.")
                break
            if opcion not in acciones:
                self.view.mostrar_mensaje("Opción no válida.")
                continue
            metodo, modifica = acciones[opcion]
            if modifica and not self.sesion.puede_modificar():
                self.view.mostrar_mensaje(
                    "Su nivel de acceso es solo de consulta.")
                continue
            self._ejecutar_accion(metodo)

    def _ejecutar_accion(self, metodo):
        try:
            metodo()
        except ERRORES_CONTROLADOS as error:
            self.view.mostrar_mensaje(f"[!] {error}")
        except Exception as error:
            self.view.mostrar_mensaje(f"[!] Error inesperado: {error}")
