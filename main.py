from config.database import Database
from controllers.main_controller import MainController
from utils.excepciones import ErrorBaseDatos


def main():
    print("Iniciando sistema")
    try:
        Database().init_db()
        MainController().ejecutar()
    except ErrorBaseDatos as error:
        print(f"\n[ERROR CRITICO] {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nSesión cerrada.")


if __name__ == "__main__":
    main()
