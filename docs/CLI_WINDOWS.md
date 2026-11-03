# Story Studio RU/UA — CLI for Windows (Sprint 09)

Run from the **project root** using PowerShell, with Python 3.10+ on PATH. No extra Python packages needed for these commands.

```powershell
python -m core.cli check .\tests\fixtures\project_v3.json
python -m core.cli preview .\tests\fixtures\project_v3.json
python -m unittest discover -s tests -v
```

To create a bundle, first ensure every referenced media file exists under the media root:

```powershell
python -m core.cli bundle .\my-project.json --media-root .\my-media --output .\exported-project
python -m core.cli verify .\exported-project
```

The destination must **not** exist. `preview` writes nothing. `check` validates the internal Python contract and prints non-fatal timeline warnings. `verify` detects missing, changed and unlisted files. Exit code 0 = success, 2 = invalid input or integrity error. The commands do not render video or create native editor timelines. Do not run untrusted scripts or projects with elevated privileges.
