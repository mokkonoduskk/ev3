from models.base_dao import BaseDAO
from models.proyecto_dao import ProyectoDAO
from models.registro_tiempo import RegistroTiempo
from utils.excepciones import ReglaNegocioError


class RegistroTiempoDAO(BaseDAO):
    TABLA = "registros_tiempo"

    @staticmethod
    def _a_objeto(f):
        return RegistroTiempo(f["fecha"], f["horas_trabajadas"],
                              f["desc_tareas"], f["id_empleado"],
                              f["id_proyecto"], f["id"])

    @staticmethod
    def crear(registro):
        if not ProyectoDAO.empleado_esta_asignado(
                registro.id_proyecto, registro.id_empleado):
            raise ReglaNegocioError(
                "El empleado no esta asignado a ese proyecto.")
        nuevo_id, _ = BaseDAO._escribir(
            "INSERT INTO registros_tiempo (fecha, horas_trabajadas, "
            "desc_tareas, id_empleado, id_proyecto) VALUES (?, ?, ?, ?, ?)",
            (registro.fecha, registro.horas_trabajadas, registro.desc_tareas,
             registro.id_empleado, registro.id_proyecto))
        registro.id = nuevo_id
        return registro

    @staticmethod
    def obtener_todos():
        return [RegistroTiempoDAO._a_objeto(f) for f in
                BaseDAO._filas("SELECT * FROM registros_tiempo ORDER BY id")]

    @staticmethod
    def obtener_por_empleado(id_empleado):
        return [RegistroTiempoDAO._a_objeto(f) for f in BaseDAO._filas(
            "SELECT * FROM registros_tiempo WHERE id_empleado = ? "
            "ORDER BY fecha", (id_empleado,))]

    @staticmethod
    def obtener_por_id(id_registro):
        fila = BaseDAO._fila(
            "SELECT * FROM registros_tiempo WHERE id = ?", (id_registro,))
        return RegistroTiempoDAO._a_objeto(fila) if fila else None

    @staticmethod
    def actualizar(registro):
        _, filas = BaseDAO._escribir(
            "UPDATE registros_tiempo SET fecha = ?, horas_trabajadas = ?, "
            "desc_tareas = ? WHERE id = ?",
            (registro.fecha, registro.horas_trabajadas, registro.desc_tareas,
             registro.id))
        return filas > 0

    @staticmethod
    def horas_por_proyecto():
        return BaseDAO._filas(
            "SELECT p.nombre AS nombre, COALESCE(SUM(r.horas_trabajadas), 0)"
            " AS total FROM proyectos p LEFT JOIN registros_tiempo r "
            "ON r.id_proyecto = p.id GROUP BY p.id ORDER BY total DESC")

    @staticmethod
    def horas_por_empleado():
        return BaseDAO._filas(
            "SELECT e.nombre AS nombre, COALESCE(SUM(r.horas_trabajadas), 0)"
            " AS total FROM empleados e LEFT JOIN registros_tiempo r "
            "ON r.id_empleado = e.id_empleado GROUP BY e.id_empleado "
            "ORDER BY total DESC")
