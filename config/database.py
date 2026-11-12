import os
import sqlite3
from contextlib import contextmanager

from utils.excepciones import ErrorBaseDatos, ErrorIntegridad

RUTA_POR_DEFECTO = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ecotech.db")

ESQUEMA = """
CREATE TABLE IF NOT EXISTS departamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    gerente_asociado TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS empleados (
    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER NOT NULL CHECK (edad BETWEEN 18 AND 99),
    rut TEXT NOT NULL UNIQUE,
    direccion TEXT NOT NULL,
    telefono INTEGER NOT NULL,
    correo TEXT NOT NULL,
    inicio_contrato TEXT NOT NULL,
    salario REAL NOT NULL CHECK (salario > 0),
    -- si se elimina el departamento el empleado sigue existiendo
    id_departamento INTEGER REFERENCES departamentos(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT NOT NULL,
    fecha_inicio TEXT NOT NULL,
    -- ubicacion y moneda de ejecucion (para clima y pagos internacionales)
    ciudad TEXT NOT NULL DEFAULT 'Santiago',
    pais TEXT NOT NULL DEFAULT 'CL',
    moneda TEXT NOT NULL DEFAULT 'CLP'
);

-- Relacion muchos-a-muchos Empleado <-> Proyecto
CREATE TABLE IF NOT EXISTS empleado_proyecto (
    id_empleado INTEGER NOT NULL REFERENCES empleados(id_empleado) ON DELETE CASCADE,
    id_proyecto INTEGER NOT NULL REFERENCES proyectos(id) ON DELETE CASCADE,
    PRIMARY KEY (id_empleado, id_proyecto)
);

CREATE TABLE IF NOT EXISTS registros_tiempo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    horas_trabajadas INTEGER NOT NULL CHECK (horas_trabajadas BETWEEN 1 AND 24),
    desc_tareas TEXT NOT NULL,
    id_empleado INTEGER NOT NULL REFERENCES empleados(id_empleado) ON DELETE CASCADE,
    -- no se puede borrar un proyecto con horas registradas
    id_proyecto INTEGER NOT NULL REFERENCES proyectos(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS administradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    rut TEXT NOT NULL UNIQUE,
    direccion TEXT NOT NULL,
    telefono INTEGER NOT NULL,
    correo TEXT NOT NULL,
    nivel_acceso TEXT NOT NULL CHECK (nivel_acceso IN ('total', 'consulta')),
    usuario TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL 
    -- hash PBKDF2, nunca texto plano
);
"""


class Database:
    _instance = None
    _db_path = RUTA_POR_DEFECTO

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    @classmethod
    def configurar_ruta(cls, ruta):
        cls._db_path = ruta

    @contextmanager
    def conectar(self):
        try:
            conexion = sqlite3.connect(self._db_path, timeout=10)
            conexion.row_factory = sqlite3.Row
            conexion.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as error:
            raise ErrorBaseDatos(
                f"No se pudo conectar a la base de datos: {error}") from error
        try:
            yield conexion
            conexion.commit()
        except sqlite3.IntegrityError as error:
            conexion.rollback()
            raise ErrorIntegridad(self._traducir(str(error))) from error
        except sqlite3.Error as error:
            conexion.rollback()
            raise ErrorBaseDatos(f"Error de base de datos: {error}") from error
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def init_db(self):
        with self.conectar() as conexion:
            conexion.executescript(ESQUEMA)
            self._migrar(conexion)

    @staticmethod
    def _migrar(conexion):
        """Agrega columnas nuevas a bases creadas con versiones anteriores
        (CREATE TABLE IF NOT EXISTS no modifica tablas ya existentes).
        Los proyectos antiguos quedan en Santiago, CL, CLP."""
        existentes = {f["name"] for f in
                      conexion.execute("PRAGMA table_info(proyectos)")}
        nuevas = {"ciudad": "Santiago", "pais": "CL", "moneda": "CLP"}
        for columna, defecto in nuevas.items():
            if columna not in existentes:
                # nombres y valores salen de este diccionario fijo, no del usuario
                conexion.execute(
                    f"ALTER TABLE proyectos ADD COLUMN {columna} "
                    f"TEXT NOT NULL DEFAULT '{defecto}'")

    @staticmethod
    def _traducir(mensaje):
        if "UNIQUE" in mensaje:
            campo = mensaje.split(".")[-1]
            return f"Ya existe un registro con ese valor ({campo})."
        if "FOREIGN KEY" in mensaje:
            return ("La operacion viola una relacion: el registro referenciado "
                    "no existe o aun esta siendo usado por otros datos.")
        if "CHECK" in mensaje:
            return "Un dato esta fuera del rango permitido."
        return f"Restriccion de integridad incumplida: {mensaje}"
