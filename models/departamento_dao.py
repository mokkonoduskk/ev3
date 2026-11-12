from models.base_dao import BaseDAO
from models.departamento import Departamento
from models.empleado_dao import EmpleadoDAO


class DepartamentoDAO(BaseDAO):
    TABLA = "departamentos"

    @staticmethod
    def _a_objeto(f):
        return Departamento(f["nombre"], f["gerente_asociado"], f["id"])

    @staticmethod
    def crear(departamento):
        nuevo_id, _ = BaseDAO._escribir(
            "INSERT INTO departamentos (nombre, gerente_asociado) VALUES (?, ?)",
            (departamento.nombre, departamento.gerente_asociado))
        departamento.id = nuevo_id
        return departamento

    @staticmethod
    def obtener_todos():
        return [DepartamentoDAO._a_objeto(f) for f in
                BaseDAO._filas("SELECT * FROM departamentos ORDER BY id")]

    @staticmethod
    def obtener_por_id(id_departamento):
        fila = BaseDAO._fila(
            "SELECT * FROM departamentos WHERE id = ?", (id_departamento,))
        return DepartamentoDAO._a_objeto(fila) if fila else None

    @staticmethod
    def obtener_con_empleados(id_departamento):
        depto = DepartamentoDAO.obtener_por_id(id_departamento)
        if depto:
            for emp in EmpleadoDAO.obtener_por_departamento(id_departamento):
                depto.agregar_empleado(emp)
        return depto

    @staticmethod
    def actualizar(departamento):
        _, filas = BaseDAO._escribir(
            "UPDATE departamentos SET nombre = ?, gerente_asociado = ? "
            "WHERE id = ?",
            (departamento.nombre, departamento.gerente_asociado,
             departamento.id))
        return filas > 0
