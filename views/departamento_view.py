from utils import validaciones as v
from views.utils import (confirmar, mostrar_lista, mostrar_menu, pedir,
                         pedir_id)


class DepartamentoView:
    @staticmethod
    def mostrar_menu():
        return mostrar_menu("GESTIÓN DE DEPARTAMENTOS", [
            "Agregar departamento", "Editar departamento",
            "Eliminar departamento", "Imprimir un departamento (con sus empleados)",
            "Imprimir todos los departamentos"])

    @staticmethod
    def formulario_nuevo_departamento():
        print("\n--- Agregar Nuevo Departamento ---")
        return {
            "nombre": pedir("Nombre del departamento",
                            lambda t: v.validar_texto(t, "El nombre")),
            "gerente_asociado": pedir(
                "Gerente asociado",
                lambda t: v.validar_texto(t, "El gerente")),
        }

    @staticmethod
    def formulario_editar_departamento(depto):
        print(f"\n--- Editando Departamento [ID: {depto.id}] ---")
        print("Presione Enter para mantener el valor actual.")
        return {
            "nombre": pedir("Nombre", lambda t: v.validar_texto(t, "Nombre"),
                            depto.nombre),
            "gerente_asociado": pedir(
                "Gerente", lambda t: v.validar_texto(t, "Gerente"),
                depto.gerente_asociado),
        }

    @staticmethod
    def solicitar_id():
        return pedir_id("Ingrese el ID del departamento")

    @staticmethod
    def mostrar_departamento(depto):
        print("\n--- Datos del Departamento ---")
        print(depto.imprimir_departamento())
        for emp in depto.obtener_empleados():
            print(f"   - {emp.imprimir_empleado()}")
        print("-" * 30)

    @staticmethod
    def mostrar_lista_departamentos(departamentos):
        mostrar_lista("Lista de Departamentos", departamentos,
                      "No hay departamentos registrados.",
                      lambda d: d.imprimir_departamento())

    @staticmethod
    def confirmar_eliminacion(nombre):
        return confirmar(f"¿Eliminar el departamento '{nombre}'? "
                         "Sus empleados quedarán sin departamento")

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(f"[DEPARTAMENTOS] {mensaje}")
