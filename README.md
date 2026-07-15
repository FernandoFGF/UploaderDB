# UploaderDB

Pipeline en Python para subir datos de SiPM a la base HWDB (dev / prod).

## Archivos

- `auto.py` — orquestador principal. Recorre `input/<BoxXX>/<TrayYYY>/` y sube cada tray a HWDB con `hwdb-upload`. Lleva estado de lo subido en `done_<env>.json` y marca `summary.xlsx` con el status `upload` (relleno azul claro).
- `docket.py` / `docket_dev.py` / `docket_prod.py` — plantillas de docket adaptadas a dev y prod.
- `diferencias_docket_dev_vs_prod.md` — referencia de las diferencias de sintaxis entre los dockets de dev y prod.

## Uso

```bash
# Modo interactivo (elige caja del menú)
python auto.py

# Modo directo (una sola tray)
python auto.py Box08 Tray000097
```

El script pregunta a qué base conectarse (`dev` o `prod`). En prod pide confirmación explícita.

## Dependencias

- Python 3.9+
- `openpyxl` (solo para actualizar el summary)
- `hwdb-upload` CLI (instalado en el entorno)

## Estructura esperada de input

```
input/
  Box08-upload/
    Tray000097-upload/
      SiPM-item-manifest.xlsx
      IV-SiPM-characterization.xlsx
      Dark-noise-SiPM-counts.xlsx
      SiPM-mass-test-results.xlsx
      ...
```

El `auto.py` detecta automáticamente las cajas (prefijo `BoxNN`) y las trays dentro.
