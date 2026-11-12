from views.utils import mostrar_lista, mostrar_menu


class ReporteView:
    @staticmethod
    def mostrar_menu():
        return mostrar_menu("REPORTES DE HORAS", [
            "Total de horas por proyecto", "Total de horas por empleado"])

    @staticmethod
    def mostrar_reporte(titulo, filas):
        mostrar_lista(titulo, filas, "Sin datos.",
                      lambda f: f"{f['nombre']:<30} {f['total']:>5} h")

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(f"[REPORTES] {mensaje}")
