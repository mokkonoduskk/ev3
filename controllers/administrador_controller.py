from controllers.base_controller import BaseController
from models.administrador import Administrador
from models.administrador_dao import AdministradorDAO
from views.administrador_view import AdministradorView

MAX_INTENTOS = 3


class AdministradorController(BaseController):
    def __init__(self, sesion=None):
        super().__init__(AdministradorView(), sesion)

    def acciones(self):
        return {1: (self.crear_administrador, True),
                2: (self.listar_administradores, False),
                3: (self.eliminar_administrador, True)}

    def autenticar(self):
        if not AdministradorDAO.hay_administradores():
            self.view.mostrar_mensaje(
                "Primer uso: cree el administrador inicial.")
            self._guardar_nuevo(forzar_total=True)
        for intento in range(1, MAX_INTENTOS + 1):
            usuario, clave = self.view.pedir_credenciales()
            admin = AdministradorDAO.obtener_por_usuario(usuario)
            if admin and admin.verificar_contraseña(clave):
                self.view.mostrar_mensaje(
                    f"Bienvenido/a, {admin.nombre} "
                    f"(acceso: {admin.nivel_acceso})")
                return admin
            self.view.mostrar_mensaje(
                f"Credenciales incorrectas ({intento}/{MAX_INTENTOS}).")
        return None

    def _guardar_nuevo(self, forzar_total=False):
        datos = self.view.formulario_nuevo_administrador(forzar_total)
        admin = Administrador(**datos)
        AdministradorDAO.crear(admin)
        self.view.mostrar_mensaje("Administrador creado exitosamente.")

    def crear_administrador(self):
        self._guardar_nuevo()

    def listar_administradores(self):
        self.view.mostrar_lista_administradores(
            AdministradorDAO.obtener_todos())

    def eliminar_administrador(self):
        id_admin = self.view.solicitar_id()
        if id_admin == self.sesion.id:
            self.view.mostrar_mensaje("No puede eliminar su propia cuenta.")
            return
        objetivo = AdministradorDAO.obtener_por_id(id_admin)
        if not objetivo:
            self.view.mostrar_mensaje("Administrador no encontrado.")
            return
        if (objetivo.puede_modificar()
                and AdministradorDAO.contar_con_acceso_total() <= 1):
            self.view.mostrar_mensaje(
                "Debe quedar al menos un administrador con acceso total.")
            return
        if self.view.confirmar_eliminacion():
            AdministradorDAO.eliminar(id_admin)
            self.view.mostrar_mensaje("Administrador eliminado.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")
