import getpass

from utils import validaciones as v
from utils.excepciones import ValidacionError


def leer_numero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")


def confirmar(mensaje):
    while True:
        resp = input(f"{mensaje} (si/no): ").strip().lower()
        if resp in ("si", "no"):
            return resp == "si"
        print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")


def pedir(mensaje, validador, actual=None):
    while True:
        sufijo = f" [{actual}]" if actual is not None else ""
        texto = input(f"{mensaje}{sufijo}: ").strip()
        if texto == "" and actual is not None:
            return actual
        try:
            return validador(texto)
        except ValidacionError as error:
            print(f"  [!] {error}")


def pedir_id(mensaje="ID"):
    return pedir(mensaje, lambda t: v.validar_entero(t, "El ID", 1))


def pedir_clave(mensaje, validar=True):
    while True:
        try:
            clave = getpass.getpass(f"{mensaje}: ")
        except (EOFError, getpass.GetPassWarning):
            clave = input(f"{mensaje}: ")
        if not validar:
            return clave
        try:
            return v.validar_contrasena(clave)
        except ValidacionError as error:
            print(f"  [!] {error}")


def mostrar_lista(titulo, items, vacio, formato=str):
    print(f"\n--- {titulo} ---")
    if not items:
        print(vacio)
    for item in items:
        print(formato(item))
    print("-" * 30)


def mostrar_menu(titulo, opciones, salir="Volver al menú principal"):
    print("\n" + "-" * 30)
    print(f" {titulo}")
    print("-" * 30)
    for numero, texto in enumerate(opciones, 1):
        print(f"{numero}.- {texto}")
    print(f"0.- {salir}")
    print("-" * 30)
    return leer_numero("Seleccione una opción: ")
