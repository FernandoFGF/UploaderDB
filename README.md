# UploaderDB — Guide for the receiving laboratory

Step-by-step guide to install and use the tool on another workstation,
without depending on the original machine's setup.

## 1. What it is and what it does

Uploads already-checked SiPM trays to the DUNE HWDB database:

1. Reads `Box##_*` folders with `Tray******_*` subfolders from `input/`.
2. Rewrites the `box = "..."` line in `docket_dev.py` / `docket_prod.py` for each tray.
3. Runs `hwdb-upload <docket>` + `hwdb-upload <docket> --submit`.
4. Tracks progress in `done_dev.json` / `done_prod.json` (skip on re-run).
5. Moves `YYYYMMDDTHHMMSS` run folders to `garbage/`.

See also `SISYPHUS_PATCH.md` (mandatory one-line fix, section 4).

## 2. Requirements

- Python 3.9+ (3.11 or 3.12 recommended).
- Linux (tested on Ubuntu) or WSL. Windows native works if `hwdb-upload` is available.
- DUNE-HWDB-Python library (provides `hwdb-upload`), sibling of this folder.

## 3. Installation (5 minutes)

1. Download this branch (no data included):

```bash
git clone -b sharing_uploader https://github.com/FernandoFGF/UploaderDB.git uploader
cd uploader
```

2. Install Python deps (only `requests`, stdlib for the rest):

```bash
python3 -m pip install -r requirements.txt
```

3. Install / locate DUNE-HWDB-Python (provides `hwdb-upload`):

```bash
ls ../DUNE-HWDB-Python*/hwdb-upload
# must exist. If not, download it from DUNE and place it next to uploader/
```

4. Apply the Sisyphus patch (section 4, mandatory).
5. Put your data in `input/` (see section 5).

## 4. Mandatory fix: Sisyphus patch

`Sisyphus` caches the GitHub release check badly: `get_latest_release_version()`
looks at `self.tag_name`, which is never set, so every `display_header()`
fires 2 requests to GitHub. With N trays you hit the 60 req/h limit and get
`KeyError: 'tag_name'`, aborting the whole upload.

File to fix (inside the HWDB library, OUTSIDE `uploader/`):

```
<DUNE-HWDB-Python>/lib/Sisyphus/Configuration/_Configuration.py
~ line 650, in get_latest_release_version()
```

```diff
      def get_latest_release_version(self):
-        if getattr(self, "tag_name", None) is None:
+        if getattr(self, "latest_release_version", None) is None:
              resp = requests.get("https://api.github.com/repos/DUNE/DUNE-HWDB-Python/releases/latest")
              self.latest_release_version = resp.json()["tag_name"]
          return self.latest_release_version
```

Full details, backup and revert instructions in `SISYPHUS_PATCH.md`.

## 5. Normal use (each batch)

1. Copy your checked data into `input/` (local, git-ignored). Must look like:

```
input/
  Box05_checked/
    Tray000138_checked/
      SiPM-item-manifest.xlsx
      IV-SiPM-characterization.xlsx
      Dark-noise-SiPM-counts.xlsx
      IV-SiPM-noise-test.xlsx
      SiPM-mass-test-results.xlsx
```

`auto.py` groups by `BoxNN` prefix, so `Box05_checked`, `Box05-upload`, etc.
all work. Only dirs starting with `Tray` are uploaded.

2. Run:

```bash
python3 auto.py                 # interactive: pick DB, pick Box from menu
python3 auto.py Box05 Tray138   # direct: numeric match, zeros ignored
```

3. Answer `dev` or `prod`. Prod asks explicit `si/yes` confirmation.
4. Progress is saved after each tray in `done_dev.json` / `done_prod.json`
   (local, git-ignored). Re-running skips with `✔ SKIP`. Delete the entry
   to force re-upload.
5. Timestamp folders (`20260727T...`) are auto-moved to `garbage/`.

Dev vs prod dockets differ only in Part Type / Test Name
(`Z.Sandbox.HWDBUnitTest.fribble/wibble` vs `D.FD-HD PDS.Module.SiPM board` /
`SiPM Mass Test Results`). `auto.py` picks the file, you never edit them
by hand (the `box = "..."` line is rewritten automatically).

## 6. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| No box found in `input/` | Empty / misnamed folder or typo | Must be `input/Box05_checked` (capital B, `BoxNN` prefix) |
| `KeyError: 'tag_name'` | Sisyphus cache bug | Apply section 4 patch |
| `hwdb-upload: command not found` | HWDB lib not on PATH | Use full path `../DUNE-HWDB-Python*/hwdb-upload` or add to PATH |
| `python: command not found` (in hwdb-upload) | Script calls `python` not `python3` | Symlink or edit shebang to `python3` |
| Tray skipped but never uploaded | Old `done_*.json` entry | Remove the tray from `done_dev/prod.json` and re-run |
| `❌ ERROR en ... -> STOP` | HWDB rejected the tray | Fix the xlsx, remove entry from `done_*.json`, re-run |
