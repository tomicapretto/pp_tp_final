import argparse

from validar import cargar_grupo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archivo")
    args = parser.parse_args()

    try:
        grupo, errores = cargar_grupo(args.archivo)
    except Exception as error:
        print(f"No se pudo leer el archivo: {error}")
        raise SystemExit(1)

    if errores:
        print("El archivo tiene errores:\n")
        for error in errores:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"Archivo valido: {grupo['nombre_grupo']}")


if __name__ == "__main__":
    main()
