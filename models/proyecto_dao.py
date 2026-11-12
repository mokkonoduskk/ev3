from models.base_dao import BaseDAO
from models.empleado_dao import EmpleadoDAO
from models.proyecto import Proyecto
from utils.excepciones import ReglaNegocioError


class ProyectoDAO(BaseDAO):
    TABLA = "proyectos"

    @staticmethod
    def _a_objeto(f):
        return Proyecto(f["nombre"], f["descripcion"], f["fecha_inicio"],
                        f["id"], f["ciudad"], f["pais"], f["moneda"])

    @staticmethod
    def crear(proyecto):
        nuevo_id, _ = BaseDAO._escribir(
            "INSERT INTO proyectos (nombre, descripcion, fecha_inicio, "
            "ciudad, pais, moneda) VALUES (?, ?, ?, ?, ?, ?)",
            (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio,
             proyecto.ciudad, proyecto.pais, proyecto.moneda))
        proyecto.id = nuevo_id
        return proyecto

    @staticmethod
    def obtener_todos():
        return [ProyectoDAO._a_objeto(f) for f in
                BaseDAO._filas("SELECT * FROM proyectos ORDER BY id")]

    @staticmethod
    def obtener_por_id(id_proyecto):
        fila = BaseDAO._fila(
            "SELECT * FROM proyectos WHERE id = ?", (id_proyecto,))
        return ProyectoDAO._a_objeto(fila) if fila else None

    @staticmethod
    def obtener_con_empleados(id_proyecto):
        proyecto = ProyectoDAO.obtener_por_id(id_proyecto)
        if proyecto:
            filas = BaseDAO._filas(
                "SELECT e.* FROM empleados e JOIN empleado_proyecto ep "
                "ON e.id_empleado = ep.id_empleado WHERE ep.id_proyecto = ?",
                (id_proyecto,))
            for f in filas:
                proyecto.asignar_empleado(EmpleadoDAO._a_objeto(f))
        return proyecto

    @staticmethod
    def actualizar(proyecto):
        _, filas = BaseDAO._escribir(
            "UPDATE proyectos SET nombre = ?, descripcion = ?, "
            "fecha_inicio = ?, ciudad = ?, pais = ?, moneda = ? "
            "WHERE id = ?",
            (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio,
             proyecto.ciudad, proyecto.pais, proyecto.moneda, proyecto.id))
        return filas > 0
    
    @staticmethod
    def asignar_empleado(id_proyecto, id_empleado):
        if not ProyectoDAO.existe(id_proyecto):
            raise ReglaNegocioError("El proyecto no existe.")
        if not EmpleadoDAO.existe(id_empleado):
            raise ReglaNegocioError("El empleado no existe.")
        BaseDAO._escribir(
            "INSERT INTO empleado_proyecto (id_empleado, id_proyecto) "
            "VALUES (?, ?)", (id_empleado, id_proyecto))

    @staticmethod
    def desasignar_empleado(id_proyecto, id_empleado):
        _, filas = BaseDAO._escribir(
            "DELETE FROM empleado_proyecto WHERE id_empleado = ? "
            "AND id_proyecto = ?", (id_empleado, id_proyecto))
        return filas > 0

    @staticmethod
    def empleado_esta_asignado(id_proyecto, id_empleado):
        return BaseDAO._fila(
            "SELECT 1 FROM empleado_proyecto WHERE id_empleado = ? "
            "AND id_proyecto = ?", (id_empleado, id_proyecto)) is not None
