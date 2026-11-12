from utils import validaciones as v
from views.utils import (confirmar, mostrar_lista, mostrar_menu, pedir,
                         pedir_id)


class EmpleadoView:
    @staticmethod
    def mostrar_menu():
        return mostrar_menu("GESTIÓN DE EMPLEADOS", [
            "Agregar empleado", "Editar empleado", "Eliminar empleado",
            "Imprimir un empleado", "Imprimir todos los empleados",
            "Buscar empleado por nombre"])

    @staticmethod
    def _elegir_departamento(departamentos, actual=None):
        print("\nDepartamentos disponibles:")
        for d in departamentos:
            print(f"{d.id}.- {d.nombre}")
        if not departamentos:
            print("No hay departamentos registrados.")
        ids_validos = {d.id for d in departamentos}
        while True:
            texto = input("ID de departamento (Enter = "
                          f"{'mantener' if actual else 'sin asignar'}, "
                          "0 = quitar): ").strip()
            if texto == "":
                return actual
            try:
                id_ = v.validar_entero(texto, "El ID", 0)
            except v.ValidacionError as error:
                print(f"  [!] {error}")
                continue
            if id_ == 0:
                return None
            if id_ in ids_validos:
                return id_
            print("  [!] Ese departamento no existe.")

    @staticmethod
    def formulario_nuevo_empleado(departamentos):
        print("\n--- Agregar Nuevo Empleado ---")
        return {
            "nombre": pedir("Nombre completo",
                            lambda t: v.validar_texto(t, "El nombre")),
            "edad": pedir("Edad", lambda t: v.validar_entero(
                t, "La edad", 18, 99)),
            "rut": pedir("RUT (ej: 12345678-5)", v.validar_rut),
            "direccion": pedir("Dirección", lambda t: v.validar_texto(
                t, "La dirección", 5, 150)),
            "telefono": pedir("Teléfono", v.validar_telefono),
            "correo": pedir("Correo", v.validar_correo),
            "inicio_contrato": pedir(
                "Inicio de contrato (AAAA-MM-DD)",
                lambda t: v.validar_fecha(t, "El inicio de contrato")),
            "salario": pedir("Salario", lambda t: v.validar_decimal(
                t, "El salario", 0)),
            "id_departamento": EmpleadoView._elegir_departamento(departamentos),
        }

    @staticmethod
    def formulario_editar_empleado(e, departamentos):
        print(f"\n--- Editando Empleado {e.nombre} ---")
        print("Presione Enter para mantener el valor actual.")
        return {
            "nombre": pedir("Nombre", lambda t: v.validar_texto(t, "Nombre"),
                            e.nombre),
            "edad": pedir("Edad", lambda t: v.validar_entero(
                t, "La edad", 18, 99), e.edad),
            "rut": pedir("RUT", v.validar_rut, e.rut),
            "direccion": pedir("Dirección", lambda t: v.validar_texto(
                t, "La dirección", 5, 150), e.direccion),
            "telefono": pedir("Teléfono", v.validar_telefono, e.telefono),
            "correo": pedir("Correo", v.validar_correo, e.correo),
            "inicio_contrato": pedir(
                "Inicio de contrato", lambda t: v.validar_fecha(
                    t, "El inicio"), e.inicio_contrato),
            "salario": pedir("Salario", lambda t: v.validar_decimal(
                t, "El salario", 0), e.salario),
            "id_departamento": EmpleadoView._elegir_departamento(
                departamentos, e.id_departamento),
        }

    @staticmethod
    def solicitar_id():
        return pedir_id("Ingrese el ID del empleado")

    @staticmethod
    def solicitar_texto_busqueda():
        return pedir("Nombre a buscar",
                     lambda t: v.validar_texto(t, "El texto", 1, 50))

    @staticmethod
    def mostrar_empleado(empleado, mostrar_salario):
        print("\n--- Datos del Empleado ---")
        print(empleado.imprimir_empleado(mostrar_salario))
        print("-" * 30)

    @staticmethod
    def mostrar_lista_empleados(empleados, mostrar_salario,
                                titulo="Lista de Empleados"):
        mostrar_lista(titulo, empleados, "No hay empleados.",
                      lambda e: e.imprimir_empleado(mostrar_salario))

    @staticmethod
    def confirmar_eliminacion(nombre):
        return confirmar(f"¿Eliminar a {nombre}? Se borrarán también sus "
                         "registros de tiempo")

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(f"[EMPLEADOS] {mensaje}")
