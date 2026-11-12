from controllers.base_controller import BaseController
from models.departamento import Departamento
from models.departamento_dao import DepartamentoDAO
from views.departamento_view import DepartamentoView


class DepartamentoController(BaseController):
    def __init__(self, sesion):
        super().__init__(DepartamentoView(), sesion)

    def acciones(self):
        return {1: (self.agregar_departamento, True),
                2: (self.editar_departamento, True),
                3: (self.eliminar_departamento, True),
                4: (self.imprimir_departamento, False),
                5: (self.imprimir_departamentos, False)}

    def agregar_departamento(self):
        datos = self.view.formulario_nuevo_departamento()
        depto = Departamento(datos["nombre"], datos["gerente_asociado"])
        DepartamentoDAO.crear(depto)
        self.view.mostrar_mensaje(
            f"Departamento agregado exitosamente con ID {depto.id}.")

    def editar_departamento(self):
        depto = DepartamentoDAO.obtener_por_id(self.view.solicitar_id())
        if not depto:
            self.view.mostrar_mensaje("Departamento no encontrado.")
            return
        datos = self.view.formulario_editar_departamento(depto)
        depto.nombre = datos["nombre"]
        depto.gerente_asociado = datos["gerente_asociado"]
        DepartamentoDAO.actualizar(depto)
        self.view.mostrar_mensaje("Departamento actualizado exitosamente.")

    def eliminar_departamento(self):
        id_depto = self.view.solicitar_id()
        depto = DepartamentoDAO.obtener_por_id(id_depto)
        if not depto:
            self.view.mostrar_mensaje("Departamento no encontrado.")
            return
        if self.view.confirmar_eliminacion(depto.nombre):
            DepartamentoDAO.eliminar(id_depto)
            self.view.mostrar_mensaje("Departamento eliminado exitosamente.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")

    def imprimir_departamento(self):
        depto = DepartamentoDAO.obtener_con_empleados(self.view.solicitar_id())
        if depto:
            self.view.mostrar_departamento(depto)
        else:
            self.view.mostrar_mensaje("Departamento no encontrado.")

    def imprimir_departamentos(self):
        self.view.mostrar_lista_departamentos(DepartamentoDAO.obtener_todos())
