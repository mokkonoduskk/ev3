from config.database import Database


class BaseDAO:
    TABLA = None
    COLUMNA_ID = "id"

    @staticmethod
    def _escribir(sql, parametros=()):
        with Database().conectar() as con:
            cursor = con.execute(sql, parametros)
            return cursor.lastrowid, cursor.rowcount

    @staticmethod
    def _filas(sql, parametros=()):
        with Database().conectar() as con:
            return con.execute(sql, parametros).fetchall()

    @staticmethod
    def _fila(sql, parametros=()):
        with Database().conectar() as con:
            return con.execute(sql, parametros).fetchone()

    @classmethod
    def eliminar(cls, id_):
        _, filas = cls._escribir(
            f"DELETE FROM {cls.TABLA} WHERE {cls.COLUMNA_ID} = ?", (id_,))
        return filas > 0

    @classmethod
    def existe(cls, id_):
        return cls._fila(
            f"SELECT 1 FROM {cls.TABLA} WHERE {cls.COLUMNA_ID} = ?",
            (id_,)) is not None
