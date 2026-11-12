import re
from datetime import datetime, date

from utils.excepciones import ValidacionError


def validar_texto(valor, campo, minimo=2, maximo=100):
    if not isinstance(valor, str):
        raise ValidacionError(f"{campo} debe ser texto.")
    valor = valor.strip()
    if not (minimo <= len(valor) <= maximo):
        raise ValidacionError(
            f"{campo} debe tener entre {minimo} y {maximo} caracteres.")
    return valor


def validar_entero(valor, campo, minimo=None, maximo=None):
    if isinstance(valor, bool):
        raise ValidacionError(f"{campo} debe ser un numero entero.")
    try:
        numero = int(str(valor).strip())
    except (ValueError, TypeError):
        raise ValidacionError(f"{campo} debe ser un numero entero.")
    if minimo is not None and numero < minimo:
        raise ValidacionError(f"{campo} no puede ser menor que {minimo}.")
    if maximo is not None and numero > maximo:
        raise ValidacionError(f"{campo} no puede ser mayor que {maximo}.")
    return numero


def validar_decimal(valor, campo, minimo=None):
    if isinstance(valor, bool):
        raise ValidacionError(f"{campo} debe ser un numero.")
    try:
        numero = float(str(valor).strip().replace(",", "."))
    except (ValueError, TypeError):
        raise ValidacionError(f"{campo} debe ser un numero.")
    if minimo is not None and numero <= minimo:
        raise ValidacionError(f"{campo} debe ser mayor que {minimo}.")
    return numero


def validar_id(valor):
    if valor is None:
        return None
    return validar_entero(valor, "ID", minimo=1)


def validar_rut(rut):
    if not isinstance(rut, str):
        raise ValidacionError("El RUT debe ser texto.")
    limpio = rut.replace(".", "").replace(" ", "").upper()
    if not re.fullmatch(r"\d{7,8}-[\dK]", limpio):
        raise ValidacionError("RUT invalido. Formato esperado: 12345678-5")
    cuerpo, dv = limpio.split("-")
    suma, multiplicador = 0, 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2
    resto = 11 - (suma % 11)
    esperado = "0" if resto == 11 else "K" if resto == 10 else str(resto)
    if dv != esperado:
        raise ValidacionError("RUT invalido: el digito verificador no coincide.")
    return limpio


def validar_correo(correo):
    correo = validar_texto(correo, "El correo", 5, 120)
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
        raise ValidacionError("Correo invalido. Ejemplo: nombre@empresa.cl")
    return correo.lower()


def validar_telefono(telefono):
    texto = str(telefono).replace(" ", "").replace("+", "")
    if not texto.isdigit():
        raise ValidacionError("El telefono solo puede contener numeros.")
    if not (8 <= len(texto) <= 11):
        raise ValidacionError("El telefono debe tener entre 8 y 11 digitos.")
    return int(texto)


def validar_fecha(fecha, campo="La fecha", permitir_futuro=True):
    try:
        fecha_dt = datetime.strptime(str(fecha).strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValidacionError(f"{campo} debe tener formato AAAA-MM-DD "
                              "(ejemplo: 2025-03-15) y ser una fecha real.")
    if not permitir_futuro and fecha_dt > date.today():
        raise ValidacionError(f"{campo} no puede estar en el futuro.")
    return fecha_dt.isoformat()


def validar_usuario(usuario):
    usuario = str(usuario).strip()
    if not re.fullmatch(r"[A-Za-z0-9_.-]{4,20}", usuario):
        raise ValidacionError(
            "El usuario debe tener 4 a 20 caracteres (letras, numeros, _ . -).")
    return usuario


def validar_contrasena(contrasena):
    if not isinstance(contrasena, str) or len(contrasena) < 8:
        raise ValidacionError("La contrasena debe tener al menos 8 caracteres.")
    if not (re.search(r"[A-Za-z]", contrasena) and re.search(r"\d", contrasena)):
        raise ValidacionError("La contrasena debe incluir letras y numeros.")
    return contrasena


NIVELES_ACCESO = ("total", "consulta")


def validar_nivel_acceso(nivel):
    nivel = str(nivel).strip().lower()
    if nivel not in NIVELES_ACCESO:
        raise ValidacionError(
            f"El nivel de acceso debe ser uno de: {', '.join(NIVELES_ACCESO)}.")
    return nivel


def validar_ciudad(ciudad):
    """Solo letras (con tildes), espacios, guiones y apostrofes: evita
    caracteres especiales antes de enviar el dato a una API externa."""
    ciudad = validar_texto(ciudad, "La ciudad", 2, 60)
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ '\-]*", ciudad):
        raise ValidacionError(
            "La ciudad solo puede contener letras, espacios, guiones y apostrofes.")
    return ciudad


def validar_codigo_pais(pais):
    """Codigo de pais ISO de 2 letras (CL, PE, AR...)."""
    pais = str(pais).strip().upper()
    if not re.fullmatch(r"[A-Z]{2}", pais):
        raise ValidacionError(
            "El pais debe ser un codigo de 2 letras (ejemplo: CL, PE, AR).")
    return pais


def validar_moneda(moneda):
    """Codigo de moneda ISO 4217 de 3 letras (CLP, USD, PEN...)."""
    moneda = str(moneda).strip().upper()
    if not re.fullmatch(r"[A-Z]{3}", moneda):
        raise ValidacionError(
            "La moneda debe ser un codigo de 3 letras (ejemplo: CLP, USD, PEN).")
    return moneda
