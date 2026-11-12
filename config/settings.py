import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    # Sin python-dotenv se usan las variables del sistema o los valores por defecto.
    pass


def _entero_positivo(nombre, defecto):
    """Lee un entero > 0 desde el entorno; si es invalido usa el valor por defecto."""
    try:
        valor = int(os.getenv(nombre, defecto))
    except (TypeError, ValueError):
        return defecto
    return valor if valor > 0 else defecto


def _booleano(nombre, defecto):
    valor = os.getenv(nombre)
    if valor is None:
        return defecto
    return valor.strip().lower() in ("true", "1", "yes", "si")


def _url_https(nombre, defecto):
    """Solo se aceptan URLs https; cualquier otra cosa vuelve al valor por defecto."""
    url = os.getenv(nombre, defecto).strip()
    return url if url.startswith("https://") else defecto


class Settings:
    REQUEST_TIMEOUT = _entero_positivo("REQUEST_TIMEOUT", 5)
    ENABLE_OFFLINE_FALLBACK = _booleano("ENABLE_OFFLINE_FALLBACK", True)

    WEATHER_API_URL = _url_https(
        "WEATHER_API_URL", "https://api.open-meteo.com/v1/forecast")
    GEOCODING_API_URL = _url_https(
        "GEOCODING_API_URL", "https://geocoding-api.open-meteo.com/v1/search")
