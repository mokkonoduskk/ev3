from utils import validaciones as v
from views.utils import (confirmar, mostrar_lista, mostrar_menu, pedir,
                         pedir_clave, pedir_id)


class AdministradorView:
    @staticmethod
    def mostrar_menu():
        return mostrar_menu("GESTIÓN DE ADMINISTRADORES", [
            "Crear administrador", "Listar administradores",
            "Eliminar administrador"])

    @staticmethod
    def pedir_credenciales():
        usuario = input("\n  Usuario: ").strip()
        clave = pedir_clave("  Contraseña", validar=False)
        return usuario, clave

    @staticmethod
    def formulario_nuevo_administrador(forzar_total=False):
        print("\n--- Nuevo Administrador ---")
        datos = {
            "nombre": pedir("Nombre completo",
                            lambda t: v.validar_texto(t, "El nombre")),
            "rut": pedir("RUT (ej: 12345678-5)", v.validar_rut),
            "direccion": pedir("Dirección", lambda t: v.validar_texto(
                t, "La dirección", 5, 150)),
            "telefono": pedir("Teléfono", v.validar_telefono),
            "correo": pedir("Correo", v.validar_correo),
        }
        datos["nivel_acceso"] = "total" if forzar_total else pedir(
            "Nivel de acceso (total/consulta)", v.validar_nivel_acceso)
        datos["usuario"] = pedir("Usuario", v.validar_usuario)
        datos["contrasena"] = pedir_clave(
            "Contraseña (mín. 8, letras y números)")
        return datos

    @staticmethod
    def solicitar_id():
        return pedir_id("Ingrese el ID del administrador")

    @staticmethod
    def mostrar_lista_administradores(administradores):
        mostrar_lista("Lista de Administradores", administradores,
                      "No hay administradores.",
                      lambda a: a.imprimir_administrador())

    @staticmethod
    def confirmar_eliminacion():
        return confirmar("¿Está seguro que desea eliminar al administrador?")

    @staticmethod
    def mostrar_mensaje(mensaje):
        print(f"[ADMINISTRADORES] {mensaje}")
