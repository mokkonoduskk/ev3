from utils import validaciones as v
from views.utils import (confirmar, mostrar_lista, mostrar_menu, pedir,
                         pedir_id)


class RegistroTiempoView:
    @staticmethod
    def mostrar_menu():
        return mostrar_menu("REGISTRO DE TIEMPO", [
            "Registrar horas", "Editar registro", "Eliminar registro",
            "Imprimir un registro", "Imprimir todos los registros",
            "Imprimir registros de un empleado"])

    @staticmethod
    def formulario_nuevo_registro():
        print("\n--- Registrar Horas Trabajadas ---")
        return {
            "fecha": pedir("Fecha (AAAA-MM-DD)", lambda t: v.validar_fecha(
                t, "La fecha", permitir_futuro=False)),
            "horas_trabajadas": pedir(
                "Horas trabajadas (1-24)",
                lambda t: v.validar_entero(t, "Las horas", 1, 24)),
            "desc_tareas": pedir("Descripción de tareas",
                                 lambda t: v.validar_texto(
                                     t, "La descripción", 5, 300)),
            "id_empleado": pedir_id("ID del empleado"),
            "id_proyecto": pedir_id("ID del proyecto"),
        }

    @staticmethod
    def formulario_editar_registro(r):
        print(f"\n--- Editando Registro [ID: {r.id}] ---")
        print("Presione Enter para mantener el valor actual.")
        return {
            "fecha": pedir("Fecha", lambda t: v.validar_fecha(
                t, "La fecha", permitir_futuro=False), r.fecha),
            "horas_trabajadas": pedir(
                "Horas", lambda t: v.validar_entero(t, "Las horas", 1, 24),
                r.horas_trabajadas),
            "desc_tareas": pedir("Descripción", lambda t: v.validar_texto(
                t, "La descripción", 5, 300), r.desc_tareas),
        }

    @staticmethod
    def solicitar_id(mensaje="Ingrese el ID del registro"):
        return pedir_id(mensaje)

    @staticmethod
    def mostrar_registro(registro):
        print("\n--- Datos del Registro ---")
        print(registro.imprimir_registro_de_tiempo())
        print("-" * 30)

    @staticmethod
    def mostrar_lista_registros(registros):
        mostrar_lista("Registros de Tiempo", registros,
                      "No hay registros.",
                      lambda r: r.imprimir_registro_de_tiempo())

    @staticmethod
    def confirmar_eliminacion():
        return confirmar("¿Está seguro que desea eliminar el registro?")

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(f"[REGISTROS] {mensaje}")
