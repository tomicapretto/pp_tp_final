import argparse
from pathlib import Path
from urllib.parse import urlparse

import yaml


ARCHIVOS_EJEMPLO = {"ejemplo.yaml", "ejemplo.yml"}


def normalizar(texto):
    return texto.strip().casefold()


def es_url(valor):
    partes = urlparse(valor)
    return partes.scheme in ("http", "https") and partes.netloc


def cargar_grupo(archivo):
    with open(archivo, encoding="utf-8") as f:
        datos = yaml.safe_load(f)

    errores = []

    if not isinstance(datos, dict):
        return None, [f"{archivo}: el YAML debe tener campos y valores"]

    nombre = datos.get("nombre_grupo")
    integrantes = datos.get("integrantes")
    repositorio = datos.get("repositorio_trabajo")

    if not nombre or not isinstance(nombre, str):
        errores.append(f"{archivo}: falta 'nombre_grupo' o esta vacio")

    if not isinstance(integrantes, list) or not integrantes:
        errores.append(f"{archivo}: 'integrantes' debe ser una lista no vacia")

    if not repositorio or not isinstance(repositorio, str) or not es_url(repositorio):
        errores.append(f"{archivo}: 'repositorio_trabajo' debe ser una URL")

    if errores:
        return None, errores

    datos["_archivo"] = archivo
    return datos, []


def archivos_yaml(carpeta):
    return sorted(
        archivo
        for archivo in Path(carpeta).glob("*")
        if archivo.suffix.lower() in (".yaml", ".yml")
    )


def cargar_grupos(carpeta="grupos", incluir_ejemplo=True):
    grupos = []
    errores = []

    for archivo in archivos_yaml(carpeta):
        if not incluir_ejemplo and archivo.name in ARCHIVOS_EJEMPLO:
            continue

        try:
            grupo, errores_archivo = cargar_grupo(archivo)
        except yaml.YAMLError as error:
            errores.append(f"{archivo}: YAML invalido: {error}")
            continue

        if errores_archivo:
            errores.extend(errores_archivo)
        else:
            grupos.append(grupo)

    revisar_repetidos = [
        grupo for grupo in grupos if grupo["_archivo"].name not in ARCHIVOS_EJEMPLO
    ]
    errores.extend(buscar_repetidos(revisar_repetidos))

    return grupos, errores


def buscar_repetidos(grupos):
    errores = []
    nombres = {}
    integrantes = {}

    for grupo in grupos:
        nombre = normalizar(grupo["nombre_grupo"])
        if nombre in nombres:
            errores.append(f"Nombre de grupo repetido: {grupo['nombre_grupo']}")
        nombres[nombre] = grupo

        for integrante in grupo["integrantes"]:
            clave = normalizar(integrante)
            if clave in integrantes:
                errores.append(f"Integrante repetido: {integrante}")
            integrantes[clave] = grupo

    return errores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grupos-dir", default="grupos")
    args = parser.parse_args()

    grupos, errores = cargar_grupos(args.grupos_dir)

    if errores:
        print("La validacion encontro errores:\n")
        for error in errores:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"Validacion correcta. Archivos revisados: {len(grupos)}")


if __name__ == "__main__":
    main()
