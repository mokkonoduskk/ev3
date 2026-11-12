import hashlib
import hmac
import os

ITERACIONES = 200_000


def hashear_contrasena(contrasena):
    sal = os.urandom(16)
    derivado = hashlib.pbkdf2_hmac(
        "sha256", contrasena.encode("utf-8"), sal, ITERACIONES)
    return f"{sal.hex()}${derivado.hex()}"


def verificar_contrasena(contrasena, almacenado):
    try:
        sal_hex, hash_hex = almacenado.split("$")
        sal = bytes.fromhex(sal_hex)
        esperado = bytes.fromhex(hash_hex)
    except ValueError:
        return False
    calculado = hashlib.pbkdf2_hmac(
        "sha256", contrasena.encode("utf-8"), sal, ITERACIONES)
    return hmac.compare_digest(calculado, esperado)
