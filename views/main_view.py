from views.utils import mostrar_menu


class MainView:
    @staticmethod
    def mostrar_bienvenida():
        print("=" * 56)
        print("   ECOTECH SOLUTIONS - Sistema de Gestión Interna")
        print("=" * 56)

    @staticmethod
    def mostrar_menu():
        return mostrar_menu("ECOTECH - MENÚ PRINCIPAL", [
            "Gestión de Departamentos",
            "Gestión de Empleados",
            "Gestión de Proyectos",
            "Registro de Tiempo",
            "Reportes de horas",
            "Gestión de Administradores"], salir="Salir")

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(f"\n[SISTEMA] {mensaje}")
