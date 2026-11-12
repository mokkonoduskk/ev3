from models.administrador import Administrador
from models.base_dao import BaseDAO


class AdministradorDAO(BaseDAO):
    TABLA = "administradores"

    @staticmethod
    def _a_objeto(f):
        return Administrador(
            f["nombre"], f["rut"], f["direccion"], f["telefono"], f["correo"],
            f["nivel_acceso"], f["usuario"], f["contrasena"], f["id"],
            contrasena_ya_hasheada=True)

    @staticmethod
    def crear(admin):
        nuevo_id, _ = BaseDAO._escribir(
            "INSERT INTO administradores (nombre, rut, direccion, telefono, "
            "correo, nivel_acceso, usuario, contrasena) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (admin.nombre, admin.rut, admin.direccion, admin.telefono,
             admin.correo, admin.nivel_acceso, admin.usuario,
             admin.obtener_contraseña()))
        admin.id = nuevo_id
        return admin

    @staticmethod
    def obtener_todos():
        return [AdministradorDAO._a_objeto(f) for f in
                BaseDAO._filas("SELECT * FROM administradores ORDER BY id")]

    @staticmethod
    def obtener_por_id(id_admin):
        fila = BaseDAO._fila(
            "SELECT * FROM administradores WHERE id = ?", (id_admin,))
        return AdministradorDAO._a_objeto(fila) if fila else None

    @staticmethod
    def obtener_por_usuario(usuario):
        fila = BaseDAO._fila(
            "SELECT * FROM administradores WHERE usuario = ?", (usuario,))
        return AdministradorDAO._a_objeto(fila) if fila else None

    @staticmethod
    def hay_administradores():
        return BaseDAO._fila(
            "SELECT 1 FROM administradores LIMIT 1") is not None

    @staticmethod
    def contar_con_acceso_total():
        return BaseDAO._fila(
            "SELECT COUNT(*) AS n FROM administradores "
            "WHERE nivel_acceso = 'total'")["n"]
