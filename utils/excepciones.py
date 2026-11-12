"""Manejo de errores y excepciones del sistema."""

class ValidacionError(ValueError):
    """El dato ingresado no cumple las reglas del sistema."""

class ErrorBaseDatos(Exception):
    """Error de acceso a la base de datos."""

class ErrorIntegridad(ErrorBaseDatos):
    """Se viola una restriccion (UNIQUE, clave foranea, CHECK...)."""

class ReglaNegocioError(Exception):
    """No se cumple una regla de negocio del dominio."""

class ErrorServicioExterno(Exception):
    """Error de acceso a un servicio externo."""

ERRORES_CONTROLADOS = (ValidacionError, ErrorBaseDatos, ReglaNegocioError, ErrorServicioExterno)
