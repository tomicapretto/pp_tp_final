import argparse
import random
from datetime import datetime
from pathlib import Path

from validar import cargar_grupos, normalizar


def generar_markdown(grupos, seed):
    fecha = datetime.now().astimezone().isoformat(timespec="seconds")

    lineas = [
        "# Orden de presentacion",
        "",
        f"- Seed usada: `{seed}`",
        f"- Fecha y hora de generacion: `{fecha}`",
        f"- Cantidad de grupos: `{len(grupos)}`",
        "",
        "## Resultado",
        "",
    ]

    for numero, grupo in enumerate(grupos, start=1):
        integrantes = ", ".join(grupo["integrantes"])
        lineas.append(f"{numero}. **{grupo['nombre_grupo']}**")
        lineas.append(f"   - Integrantes: {integrantes}")
        lineas.append(f"   - Repositorio: {grupo['repositorio_trabajo']}")

    return "\n".join(lineas) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True)
    parser.add_argument("--grupos-dir", default="grupos")
    parser.add_argument("--salida", default="orden-presentacion.md")
    args = parser.parse_args()

    grupos, errores = cargar_grupos(args.grupos_dir, incluir_ejemplo=False)

    if errores:
        print("No se puede sortear porque hay errores:\n")
        for error in errores:
            print(f"- {error}")
        raise SystemExit(1)

    grupos.sort(key=lambda grupo: normalizar(grupo["nombre_grupo"]))
    random.Random(args.seed).shuffle(grupos)

    Path(args.salida).write_text(generar_markdown(grupos, args.seed), encoding="utf-8")
    print(f"Sorteo generado en {args.salida}")


if __name__ == "__main__":
    main()
