from controllers.base_controller import BaseController
from models.departamento_dao import DepartamentoDAO
from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO
from views.empleado_view import EmpleadoView


class EmpleadoController(BaseController):
    def __init__(self, sesion):
        super().__init__(EmpleadoView(), sesion)

    def acciones(self):
        return {1: (self.agregar_empleado, True),
                2: (self.editar_empleado, True),
                3: (self.eliminar_empleado, True),
                4: (self.imprimir_empleado, False),
                5: (self.imprimir_empleados, False),
                6: (self.buscar_empleados, False)}

    def _ver_salario(self):
        return self.sesion.puede_modificar()

    def agregar_empleado(self):
        datos = self.view.formulario_nuevo_empleado(
            DepartamentoDAO.obtener_todos())
        empleado = Empleado(**datos)
        EmpleadoDAO.crear(empleado)
        self.view.mostrar_mensaje(
            f"Empleado agregado exitosamente con ID {empleado.id_empleado}.")

    def editar_empleado(self):
        empleado = EmpleadoDAO.obtener_por_id(self.view.solicitar_id())
        if not empleado:
            self.view.mostrar_mensaje("Empleado no encontrado.")
            return
        datos = self.view.formulario_editar_empleado(
            empleado, DepartamentoDAO.obtener_todos())
        empleado.nombre = datos["nombre"]
        empleado.edad = datos["edad"]
        empleado.rut = datos["rut"]
        empleado.direccion = datos["direccion"]
        empleado.telefono = datos["telefono"]
        empleado.correo = datos["correo"]
        empleado.inicio_contrato = datos["inicio_contrato"]
        empleado.salario = datos["salario"]
        empleado.id_departamento = datos["id_departamento"]
        EmpleadoDAO.actualizar(empleado)
        self.view.mostrar_mensaje("Empleado actualizado exitosamente.")

    def eliminar_empleado(self):
        id_empleado = self.view.solicitar_id()
        empleado = EmpleadoDAO.obtener_por_id(id_empleado)
        if not empleado:
            self.view.mostrar_mensaje("Empleado no encontrado.")
            return
        if self.view.confirmar_eliminacion(empleado.nombre):
            EmpleadoDAO.eliminar(id_empleado)
            self.view.mostrar_mensaje("Empleado eliminado exitosamente.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")

    def imprimir_empleado(self):
        empleado = EmpleadoDAO.obtener_por_id(self.view.solicitar_id())
        if empleado:
            self.view.mostrar_empleado(empleado, self._ver_salario())
        else:
            self.view.mostrar_mensaje("Empleado no encontrado.")

    def imprimir_empleados(self):
        self.view.mostrar_lista_empleados(
            EmpleadoDAO.obtener_todos(), self._ver_salario())

    def buscar_empleados(self):
        texto = self.view.solicitar_texto_busqueda()
        self.view.mostrar_lista_empleados(
            EmpleadoDAO.buscar_por_nombre(texto), self._ver_salario(),
            titulo=f"Resultados para '{texto}'")
