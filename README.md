# Sorteo de presentaciones

Este repositorio se usa para organizar el sorteo del orden de presentación de los trabajos finales del curso.

Cada grupo debe agregar un archivo YAML con sus datos dentro de la carpeta `grupos/`.
Cuando todos los grupos estén mergeados en `main`, se ejecutará manualmente un _workflow_ de GitHub Actions que genera el archivo `orden-presentacion.md` y lo guarda en el repositorio.

## Estructura

```text
.
├── .github
│   └── workflows
│       ├── sortear.yml
│       └── validar.yml
├── .gitignore
├── .python-version
├── README.md
├── grupos
│   └── ejemplo.yaml
├── pyproject.toml
├── scripts
│   ├── sortear.py
│   ├── validar.py
│   └── validar_archivo.py
└── uv.lock
```

## Instrucciones

1.  Clonar el repositorio

    ```bash
    git clone <url>
    cd sorteo-presentaciones
    ```

    Reemplacen `<url>` por la URL real del repositorio.

2.  Instalar dependencias con `uv`

    Este proyecto usa `uv` para administrar Python y las dependencias. Ejecutar:

    ```bash
    uv sync
    ```

3.  Crear una rama para el grupo

    ```bash
    git switch -c <nombre-de-rama>
    ```

4.  Crear el archivo YAML del grupo

    Cada grupo debe crear un solo archivo nuevo dentro de `grupos/`.

    El nombre del archivo debe identificar al grupo. Por ejemplo:

    ```text
    grupos/<nombre-de-grupo>.yaml
    ```

    El contenido debe tener esta forma:

    ```yaml
    nombre_grupo: Nombre de grupo
    integrantes:
      - Ana Pérez
      - Bruno Gómez
      - Carla Ruiz
    repositorio_trabajo: https://github.com/usr/repo
    ```

    Campos requeridos:

    - `nombre_grupo`: nombre del grupo.
    - `integrantes`: lista con los nombres de las personas que integran el grupo.
    - `repositorio_trabajo`: URL del repositorio del trabajo final.

5.  Validar el archivo del grupo

    Antes de hacer commit, validen el archivo que crearon:

    ```bash
    uv run python scripts/validar_archivo.py grupos/<nombre-de-grupo>.yaml
    ```

    Si el archivo está bien, van a ver un mensaje indicando que la validación fue exitosa.

    También pueden validar todos los archivos de la carpeta `grupos/`:

    ```bash
    uv run python scripts/validar.py
    ```

6.  Hacer commit y push

    ```bash
    git status
    git add grupos/<nombre-de-grupo>.yaml
    git commit -m "Agregar grupo ..."
    git push -u origin <nombre-de-rama>
    ```

7.  Abrir un Pull Request

    Desde GitHub, abran un Pull Request desde la rama del grupo hacia `main`.

    GitHub Actions va a ejecutar automáticamente la validación. Si la validación falla, revisen el error, corrijan el archivo, hagan un nuevo commit y vuelvan a pushear la rama.

## Reglas importantes

- Cada grupo debe crear solo un archivo nuevo dentro de `grupos/`.
- No editen archivos de otros grupos.
- No editen `scripts/`, `.github/workflows/`, `pyproject.toml` ni `uv.lock`.
- No borren ni modifiquen `grupos/ejemplo.yaml`.
- No usen nombres de grupo repetidos.
- No repitan integrantes entre grupos.

## Reproducibilidad del sorteo

Para reproducir el mismo sorteo en una computadora local:

```bash
uv sync
uv run python scripts/sortear.py --seed "curso-python-2026"
```

Si los archivos dentro de `grupos/` son los mismos y la semilla es la misma, el orden generado será el mismo.
