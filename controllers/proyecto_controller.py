from controllers.base_controller import BaseController
from models.proyecto import Proyecto
from models.proyecto_dao import ProyectoDAO
from views.proyecto_view import ProyectoView


class ProyectoController(BaseController):
    def __init__(self, sesion):
        super().__init__(ProyectoView(), sesion)

    def acciones(self):
        return {1: (self.agregar_proyecto, True),
                2: (self.editar_proyecto, True),
                3: (self.eliminar_proyecto, True),
                4: (self.imprimir_proyecto, False),
                5: (self.imprimir_proyectos, False),
                6: (self.asignar_empleado, True),
                7: (self.quitar_empleado, True)}

    def agregar_proyecto(self):
        datos = self.view.formulario_nuevo_proyecto()
        proyecto = Proyecto(datos["nombre"], datos["descripcion"],
                            datos["fecha_inicio"], ciudad=datos["ciudad"],
                            pais=datos["pais"], moneda=datos["moneda"])
        ProyectoDAO.crear(proyecto)
        self.view.mostrar_mensaje(
            f"Proyecto agregado exitosamente con ID {proyecto.id}.")

    def editar_proyecto(self):
        proyecto = ProyectoDAO.obtener_por_id(self.view.solicitar_id())
        if not proyecto:
            self.view.mostrar_mensaje("Proyecto no encontrado.")
            return
        datos = self.view.formulario_editar_proyecto(proyecto)
        proyecto.nombre = datos["nombre"]
        proyecto.descripcion = datos["descripcion"]
        proyecto.fecha_inicio = datos["fecha_inicio"]
        proyecto.ciudad = datos["ciudad"]
        proyecto.pais = datos["pais"]
        proyecto.moneda = datos["moneda"]
        ProyectoDAO.actualizar(proyecto)
        self.view.mostrar_mensaje("Proyecto actualizado exitosamente.")

    def eliminar_proyecto(self):
        id_proyecto = self.view.solicitar_id()
        proyecto = ProyectoDAO.obtener_por_id(id_proyecto)
        if not proyecto:
            self.view.mostrar_mensaje("Proyecto no encontrado.")
            return
        if self.view.confirmar_eliminacion(proyecto.nombre):
            ProyectoDAO.eliminar(id_proyecto)
            self.view.mostrar_mensaje("Proyecto eliminado exitosamente.")
        else:
            self.view.mostrar_mensaje("Operación cancelada.")

    def imprimir_proyecto(self):
        proyecto = ProyectoDAO.obtener_con_empleados(self.view.solicitar_id())
        if proyecto:
            self.view.mostrar_proyecto(proyecto, self.sesion.puede_modificar())
        else:
            self.view.mostrar_mensaje("Proyecto no encontrado.")

    def imprimir_proyectos(self):
        self.view.mostrar_lista_proyectos(ProyectoDAO.obtener_todos())

    def asignar_empleado(self):
        ProyectoDAO.asignar_empleado(self.view.solicitar_id(),
                                     self.view.solicitar_id_empleado())
        self.view.mostrar_mensaje("Empleado asignado al proyecto.")

    def quitar_empleado(self):
        quitado = ProyectoDAO.desasignar_empleado(
            self.view.solicitar_id(), self.view.solicitar_id_empleado())
        self.view.mostrar_mensaje(
            "Asignación eliminada." if quitado
            else "Ese empleado no estaba asignado al proyecto.")
