from models.base_dao import BaseDAO
from models.empleado import Empleado


class EmpleadoDAO(BaseDAO):
    TABLA = "empleados"
    COLUMNA_ID = "id_empleado"

    @staticmethod
    def _a_objeto(f):
        return Empleado(f["nombre"], f["edad"], f["rut"], f["direccion"],
                        f["telefono"], f["correo"], f["inicio_contrato"],
                        f["salario"], f["id_empleado"], f["id_departamento"])

    @staticmethod
    def _datos(e):
        return (e.nombre, e.edad, e.rut, e.direccion, e.telefono, e.correo,
                e.inicio_contrato, e.salario, e.id_departamento)

    @staticmethod
    def crear(empleado):
        nuevo_id, _ = BaseDAO._escribir(
            "INSERT INTO empleados (nombre, edad, rut, direccion, telefono, "
            "correo, inicio_contrato, salario, id_departamento) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", EmpleadoDAO._datos(empleado))
        empleado.id_empleado = nuevo_id
        return empleado

    @staticmethod
    def obtener_todos():
        return [EmpleadoDAO._a_objeto(f) for f in BaseDAO._filas(
            "SELECT * FROM empleados ORDER BY id_empleado")]

    @staticmethod
    def obtener_por_departamento(id_departamento):
        return [EmpleadoDAO._a_objeto(f) for f in BaseDAO._filas(
            "SELECT * FROM empleados WHERE id_departamento = ? "
            "ORDER BY id_empleado", (id_departamento,))]

    @staticmethod
    def buscar_por_nombre(texto):
        return [EmpleadoDAO._a_objeto(f) for f in BaseDAO._filas(
            "SELECT * FROM empleados WHERE nombre LIKE ? ORDER BY nombre",
            (f"%{texto}%",))]

    @staticmethod
    def obtener_por_id(id_empleado):
        fila = BaseDAO._fila(
            "SELECT * FROM empleados WHERE id_empleado = ?", (id_empleado,))
        return EmpleadoDAO._a_objeto(fila) if fila else None

    @staticmethod
    def actualizar(empleado):
        _, filas = BaseDAO._escribir(
            "UPDATE empleados SET nombre = ?, edad = ?, rut = ?, direccion = ?,"
            " telefono = ?, correo = ?, inicio_contrato = ?, salario = ?, "
            "id_departamento = ? WHERE id_empleado = ?",
            EmpleadoDAO._datos(empleado) + (empleado.id_empleado,))
        return filas > 0
