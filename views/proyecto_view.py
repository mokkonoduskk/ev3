from utils import validaciones as v
from views.utils import (confirmar, mostrar_lista, mostrar_menu, pedir,
                         pedir_id)


class ProyectoView:
    @staticmethod
    def mostrar_menu():
        return mostrar_menu("GESTIÓN DE PROYECTOS", [
            "Agregar proyecto", "Editar proyecto", "Eliminar proyecto",
            "Imprimir un proyecto (con empleados)",
            "Imprimir todos los proyectos",
            "Asignar empleado a proyecto", "Quitar empleado de proyecto"])

    @staticmethod
    def formulario_nuevo_proyecto():
        print("\n--- Agregar Nuevo Proyecto ---")
        return {
            "nombre": pedir("Nombre", lambda t: v.validar_texto(t, "El nombre")),
            "descripcion": pedir("Descripción", lambda t: v.validar_texto(
                t, "La descripción", 5, 300)),
            "fecha_inicio": pedir("Fecha de inicio (AAAA-MM-DD)",
                                  lambda t: v.validar_fecha(
                                      t, "La fecha de inicio")),
            "ciudad": pedir("Ciudad de ejecución", v.validar_ciudad),
            "pais": pedir("País (código de 2 letras, ej: CL, PE)",
                          v.validar_codigo_pais),
            "moneda": pedir("Moneda local (código de 3 letras, ej: CLP, USD)",
                            v.validar_moneda),
        }

    @staticmethod
    def formulario_editar_proyecto(p):
        print(f"\n--- Editando Proyecto [ID: {p.id}] ---")
        print("Presione Enter para mantener el valor actual.")
        return {
            "nombre": pedir("Nombre", lambda t: v.validar_texto(t, "Nombre"),
                            p.nombre),
            "descripcion": pedir("Descripción", lambda t: v.validar_texto(
                t, "La descripción", 5, 300), p.descripcion),
            "fecha_inicio": pedir("Fecha de inicio", lambda t: v.validar_fecha(
                t, "La fecha"), p.fecha_inicio),
            "ciudad": pedir("Ciudad", v.validar_ciudad, p.ciudad),
            "pais": pedir("País (2 letras)", v.validar_codigo_pais, p.pais),
            "moneda": pedir("Moneda (3 letras)", v.validar_moneda, p.moneda),
        }

    @staticmethod
    def solicitar_id(mensaje="Ingrese el ID del proyecto"):
        return pedir_id(mensaje)

    @staticmethod
    def solicitar_id_empleado():
        return pedir_id("Ingrese el ID del empleado")

    @staticmethod
    def mostrar_proyecto(proyecto, mostrar_salario):
        print("\n--- Datos del Proyecto ---")
        print(proyecto.imprimir_proyecto())
        if not proyecto.obtener_empleados():
            print("   (sin empleados asignados)")
        for emp in proyecto.obtener_empleados():
            print(f"   - {emp.imprimir_empleado(mostrar_salario)}")
        print("-" * 30)

    @staticmethod
    def mostrar_lista_proyectos(proyectos):
        mostrar_lista("Lista de Proyectos", proyectos,
                      "No hay proyectos registrados.",
                      lambda p: p.imprimir_proyecto())

    @staticmethod
    def confirmar_eliminacion(nombre):
        return confirmar(f"¿Está seguro que desea eliminar el proyecto "
                         f"'{nombre}'?")

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(f"[PROYECTOS] {mensaje}")
