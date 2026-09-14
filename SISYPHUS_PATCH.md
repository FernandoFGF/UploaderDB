# Sisyphus patch

## What it fixes

`Sisyphus` has a caching system to avoid repeated calls to the
GitHub API. In theory, `display_header()` should only query
`https://api.github.com/repos/DUNE/DUNE-HWDB-Python/releases/latest` once
a day and use the cached value for the rest of the day. In practice, the
cache was broken: the condition deciding whether we already had a
cached value looked at an attribute (`self.tag_name`) that is **never set**
anywhere in the code. Result: every call to
`display_header()` made 2 requests to GitHub instead of 0. Multiplied
by N trays and the GitHub rate limit (60 req/h without a token), the
`KeyError: 'tag_name'` showed up sooner or later and aborted the whole
upload before processing anything.

The bug was in `Sisyphus/Configuration/_Configuration.py:650`. The
correct code (the one the cache sets) is `self.latest_release_version`.

## Modified files

`~/HWDBSiPM/DUNE-HWDB-Python-1.2.4.2/lib/Sisyphus/Configuration/_Configuration.py`
(outside `uploader/`, inside the `DUNE-HWDB-Python` library
installed in the environment).

Backups of the originals:
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

## What it does NOT change

- `uploader/auto.py` was not touched.
- No new file was created in `uploader/`.
- The upload logic (`hwdb-upload docket_prod.py`, `--submit`, etc.) is
  exactly the same.
- `display_header()` runs the same way, prints the banner and (if there
  is a new version) the `Notice`. The only difference is that it now uses
  the cache correctly.
- The `newer_version_exists()` function was not touched.
- The cache system in `~/.sisyphus/config.json` (lines
  545-558 of `_Configuration.py`) was not touched; the fix makes that
  cache **work** for the first time.

## Verification

Test run (in `C:\Users\Ferna\AppData\Local\Temp\opencode\test_cache.py`):
mocks `requests.get`, calls `display_header()` 3 times, counts
HTTP calls. Result:

```
[TEST] GitHub calls after display_header 1: 1
[TEST] GitHub calls after display_header 2: 1
[TEST] GitHub calls after display_header 3: 1
[TEST] OK: cache works, 1 single GitHub call for 3 display_header invocations
```

With the original bug it would be 6 calls (2 per display_header x 3). With
the fix: just 1.

## How to revert

To go back to the original `_Configuration.py`:

```bash
mv /home/ugrlab/HWDBSiPM/DUNE-HWDB-Python-1.2.4.2/lib/Sisyphus/Configuration/_Configuration.py.bak \
   /home/ugrlab/HWDBSiPM/DUNE-HWDB-Python-1.2.4.2/lib/Sisyphus/Configuration/_Configuration.py
```

If you update `DUNE-HWDB-Python` (pip, git pull, etc.) the patch will be
lost and you will have to re-apply it.
