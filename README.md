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

Secondary files:

- `docket_dev.py`: docket for dev/sandbox DB (`Z.Sandbox.HWDBUnitTest`).
- `docket_prod.py`: docket for production DB (`D.FD-HD PDS.Module.SiPM board`).
- `SISYPHUS_PATCH.md`: mandatory one-line fix in the HWDB library (see section 4).
- `HWDB_Instructions_and_Commands-1.pdf`: official reference (optional, not in git).

## 2. Requirements

- Python 3.9+ (3.11 or 3.12 recommended).
- Linux (tested on Ubuntu) or WSL. Windows native works if `hwdb-upload` is available.
- DUNE-HWDB-Python library (provides `hwdb-upload`), sibling of this folder.
- Nothing to compile.

Check your Python:

```bash
python3 --version
```

## 3. Installation (5 minutes)

1. Download this branch (no data included):

```bash
git clone -b sharing_uploader https://github.com/FernandoFGF/UploaderDB.git uploader
cd uploader
```

Or as zip: `git archive --format=zip --output=uploader-export.zip sharing_uploader`.

2. Install Python deps (only `requests`, stdlib for the rest):

```bash
python3 -m pip install -r requirements.txt
```

3. Install / locate DUNE-HWDB-Python (provides `hwdb-upload`):

```bash
ls ../DUNE-HWDB-Python-1.2.4.2/hwdb-upload
# must exist. If not, download it from DUNE and place it next to uploader/
```

4. Apply the Sisyphus patch (section 4, mandatory).
5. Put your data in `input/` (see section 5). `input/`, `garbage/`,
   `done_*.json` and `latest` are local and never committed.

## 4. Mandatory fix: Sisyphus patch (they DO have to do it)

`Sisyphus` caches the GitHub release check badly: `get_latest_release_version()`
looks at `self.tag_name`, which is never set, so every `display_header()`
fires 2 requests to GitHub. With N trays you hit the 60 req/h limit and get
`KeyError: 'tag_name'`, aborting the whole upload.

Full details in `SISYPHUS_PATCH.md`. Summary:

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

Backup first, then re-apply after every library update (pip / git pull wipes it).

Verification: call `display_header()` 3x with mocked `requests.get` → 1 HTTP
call total (before: 6). See `SISYPHUS_PATCH.md`.

What it does NOT change: `auto.py` logic, docket syntax, `--submit` flow,
`newer_version_exists()`, `~/.sisyphus/config.json` cache. It just makes
the existing cache work.

## 5. Normal use (each batch)

1. Copy your checked data into `input/`. Must look like:

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
4. Progress is saved after each tray in `done_dev.json` / `done_prod.json`.
   Re-running skips with `✔ SKIP`. Delete the entry to force re-upload.
5. Timestamp folders (`20260727T...`) are auto-moved to `garbage/`.

Dev vs prod dockets differ only in Part Type / Test Name
(`Z.Sandbox.HWDBUnitTest.fribble/wibble` vs `D.FD-HD PDS.Module.SiPM board` /
`SiPM Mass Test Results`). `auto.py` picks the file, you never edit them
by hand (the `box = "..."` line is rewritten automatically).

## 6. Folder structure (what is sent and what is not)

```
uploader/
  auto.py                <- orchestrator
  docket_dev.py          <- dev docket (box is auto-rewritten)
  docket_prod.py         <- prod docket (box is auto-rewritten)
  SISYPHUS_PATCH.md      <- mandatory library fix
  requirements.txt       <- dependencies
  README.md              <- this guide
  input/Box*             <- your data (local, never committed)
  garbage/*              <- run trash (local, never committed)
  done_*.json            <- upload state (local, never committed)
  latest                 <- symlink to last run (local, never committed)
```

Your data and state files (`input/`, `garbage/`, `done_*.json`, `latest`)
are local only and never committed to git.

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `No se han detectado cajas en input/` | Empty / misnamed folder | Must be `input/Box05_checked` (capital B, `BoxNN` prefix) |
| `Box 'Box08' no encontrado` | Typo in direct mode | `python3 auto.py Box08 Tray000097`, check menu list first |
| `KeyError: 'tag_name'` | Sisyphus cache bug | Apply section 4 patch |
| `hwdb-upload: command not found` | HWDB lib not on PATH | Use full path `../DUNE-HWDB-Python-1.2.4.2/hwdb-upload` or add to PATH |
| `python: command not found` (in hwdb-upload) | Script calls `python` not `python3` | Symlink or edit shebang to `python3` |
| Tray skipped but never uploaded | Old `done_*.json` entry | Remove the tray from `done_dev/prod.json` and re-run |
| `❌ ERROR en ... -> STOP` | HWDB rejected the tray | Fix the xlsx, remove entry from `done_*.json`, re-run |

## 8. Notes

- No external spreadsheet: upload progress is tracked only in local
  `done_dev.json` / `done_prod.json`. No `openpyxl` needed.
- The `box = "..."` line in the dockets is rewritten automatically by
  `auto.py`; you never edit it by hand.
- `SISYPHUS_PATCH.md` must be applied to your own copy of
  `DUNE-HWDB-Python` (a file outside this repo).
