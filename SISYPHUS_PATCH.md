# Parche en Sisyphus

## Qué aplicaba

`Sisyphus` tiene un sistema de caché para evitar llamadas repetidas a la
API de GitHub. En teoría, `display_header()` solo debería consultar
`https://api.github.com/repos/DUNE/DUNE-HWDB-Python/releases/latest` una
vez al día y usar el valor cacheado el resto del día. En la práctica, el
caché estaba roto: la condición que decidía si ya teníamos valor
cacheado miraba un atributo (`self.tag_name`) que **nunca se setea** en
ningún sitio del código. Resultado: cada llamada a
`display_header()` hacía 2 peticiones a GitHub en vez de 0. Multiplicado
por N trays y el rate limit de GitHub (60 req/h sin token), el
`KeyError: 'tag_name'` aparecía tarde o temprano y abortaba el upload
entero antes de procesar nada.

El bug estaba en `Sisyphus/Configuration/_Configuration.py:650`. El
código correcto (el que el caché setea) es `self.latest_release_version`.

## Archivos modificados

`~/HWDBSiPM/DUNE-HWDB-Python-1.2.4.2/lib/Sisyphus/Configuration/_Configuration.py`
(fuera de `uploader/`, dentro de la librería `DUNE-HWDB-Python`
instalada en el entorno).

Backups de los originales:
- `~/HWDBSiPM/DUNE-HWDB-Python-1.2.4.2/lib/Sisyphus/Configuration/_Configuration.py.bak`

## Diff

```diff
     def get_latest_release_version(self):
-        if getattr(self, "tag_name", None) is None:
+        if getattr(self, "latest_release_version", None) is None:
             resp = requests.get("https://api.github.com/repos/DUNE/DUNE-HWDB-Python/releases/latest")
             self.latest_release_version = resp.json()["tag_name"]
         return self.latest_release_version
```

## Qué NO modifica

- `uploader/auto.py` no se ha tocado.
- No se ha creado ningún archivo nuevo en `uploader/`.
- La lógica de carga (`hwdb-upload docket_prod.py`, `--submit`, etc.) es
  exactamente la misma.
- El `display_header()` se ejecuta igual, imprime el banner y (si hay
  versión nueva) el `Notice`. La única diferencia es que ahora usa el
  caché correctamente.
- La función `newer_version_exists()` no se ha tocado.
- El sistema de caché del archivo `~/.sisyphus/config.json` (líneas
  545-558 de `_Configuration.py`) no se ha tocado; el fix hace que ese
  caché **funcione** por primera vez.

## Verificación

Test ejecutado (en `C:\Users\Ferna\AppData\Local\Temp\opencode\test_cache.py`):
mockea `requests.get`, llama a `display_header()` 3 veces, cuenta
llamadas HTTP. Resultado:

```
[TEST] Llamadas a GitHub despues de display_header 1: 1
[TEST] Llamadas a GitHub despues de display_header 2: 1
[TEST] Llamadas a GitHub despues de display_header 3: 1
[TEST] OK: la cache funciona, 1 sola llamada a GitHub para 3 invocaciones de display_header
```

Con el bug original serían 6 llamadas (2 por display_header × 3). Con el
fix: 1 sola.

## Cómo revertir

Para volver a la versión original de `_Configuration.py`:

```bash
mv /home/ugrlab/HWDBSiPM/DUNE-HWDB-Python-1.2.4.2/lib/Sisyphus/Configuration/_Configuration.py.bak \
   /home/ugrlab/HWDBSiPM/DUNE-HWDB-Python-1.2.4.2/lib/Sisyphus/Configuration/_Configuration.py
```

Si actualizas `DUNE-HWDB-Python` (pip, git pull, etc.) el parche se
perderá y tendrás que reaplicarlo.
