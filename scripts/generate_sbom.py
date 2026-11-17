"""Generate a deterministic CycloneDX 1.5 SBOM from the audited license CSVs.

Single source of truth: LICENSES/DEPENDENCY_LICENSES.csv,
LICENSES/AI_MODELS_AND_SERVICES.csv and LICENSES/ASSET_REGISTER.csv
(Sprint 27 Stage 1 audit, ADR-0009). The output is byte-stable for identical
inputs, so `--check` can fail a CI run when registers and SBOM drift apart.
No third-party packages are used to build it.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LICENSES = ROOT / "LICENSES"

DEPENDENCY_CSV = LICENSES / "DEPENDENCY_LICENSES.csv"
MODELS_CSV = LICENSES / "AI_MODELS_AND_SERVICES.csv"
ASSETS_CSV = LICENSES / "ASSET_REGISTER.csv"
DEFAULT_OUTPUT = LICENSES / "SBOM.cdx.json"

BOM_FORMAT = "CycloneDX"
SPEC_VERSION = "1.5"
PROJECT_NAME = "Story-Studio-RU-UA"


def read_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def _properties(register: str, row: dict, keys: tuple[str, ...]) -> list[dict]:
    props = [{"name": "storystudio:register", "value": register}]
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            props.append({"name": "storystudio:" + key.replace("_", "-"), "value": value})
    return props


def dependency_component(row: dict) -> dict:
    name = row["package"].strip()
    version = row["version"].strip()
    purl = "pkg:pypi/" + name.lower() + "@" + version.replace("+", "%2B")
    licenses = []
    license_id = (row.get("license") or "").strip()
    if license_id:
        licenses.append({"license": {"name": license_id}})
    return {
        "type": "library",
        "bom-ref": purl,
        "name": name,
        "version": version,
        "purl": purl,
        "licenses": licenses,
        "properties": _properties("DEPENDENCY_LICENSES", row,
                                  ("source", "commercial_use", "status", "notes")),
    }


def model_component(row: dict) -> dict:
    name = row["provider_or_model"].strip()
    version = (row.get("version") or "").strip()
    ref = "storystudio:model/" + name.lower().replace(" ", "-")
    return {
        "type": "machine-learning-model",
        "bom-ref": ref,
        "name": name,
        "version": version,
        "properties": _properties("AI_MODELS_AND_SERVICES", row,
                                  ("source", "terms_url", "commercial_use",
                                   "data_handling", "status")),
    }


def asset_component(row: dict) -> dict:
    path = row["path"].strip()
    ref = "storystudio:asset/" + path.replace("\\", "/")
    return {
        "type": "file",
        "bom-ref": ref,
        "name": path,
        "properties": _properties("ASSET_REGISTER", row,
                                  ("type", "source", "license", "commercial_use",
                                   "redistribution", "status", "notes")),
    }


def build_components(dependency_csv: Path, models_csv: Path,
                     assets_csv: Path) -> list[dict]:
    components: list[dict] = []
    seen: set[str] = set()
    for reader, register in ((dependency_component, dependency_csv),
                             (model_component, models_csv),
                             (asset_component, assets_csv)):
        for row in read_rows(register):
            if not any((value or "").strip() for value in row.values()):
                continue  # skip fully empty spreadsheet rows
            component = reader(row)
            if component["bom-ref"] in seen:
                raise ValueError("Duplicate bom-ref in SBOM: " + component["bom-ref"])
            seen.add(component["bom-ref"])
            components.append(component)
    components.sort(key=lambda c: (c["type"], c["name"].lower(), c.get("version", "")))
    return components


def _serial_number(components: list[dict]) -> str:
    canonical = json.dumps(components, sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, digest))


def build_bom(dependency_csv: Path = DEPENDENCY_CSV, models_csv: Path = MODELS_CSV,
              assets_csv: Path = ASSETS_CSV) -> dict:
    components = build_components(dependency_csv, models_csv, assets_csv)
    return {
        "bomFormat": BOM_FORMAT,
        "specVersion": SPEC_VERSION,
        "serialNumber": _serial_number(components),
        "version": 1,
        "metadata": {
            "component": {
                "type": "application",
                "name": PROJECT_NAME,
                "description": "Windows-first RU/UA video story studio",
                "properties": [
                    {"name": "storystudio:registers",
                     "value": "DEPENDENCY_LICENSES, AI_MODELS_AND_SERVICES, ASSET_REGISTER"},
                ],
            },
        },
        "components": components,
    }


def render_bom(bom: dict) -> str:
    return json.dumps(bom, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def write_sbom(output: Path = DEFAULT_OUTPUT, dependency_csv: Path = DEPENDENCY_CSV,
               models_csv: Path = MODELS_CSV, assets_csv: Path = ASSETS_CSV) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_bom(build_bom(dependency_csv, models_csv, assets_csv)),
                      encoding="utf-8", newline="\n")
    return output


def check_sbom(output: Path = DEFAULT_OUTPUT, dependency_csv: Path = DEPENDENCY_CSV,
               models_csv: Path = MODELS_CSV, assets_csv: Path = ASSETS_CSV) -> bool:
    if not output.is_file():
        return False
    return output.read_text(encoding="utf-8-sig") == render_bom(
        build_bom(dependency_csv, models_csv, assets_csv))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Build or verify LICENSES/SBOM.cdx.json from the audited CSVs")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true",
                        help="verify the existing SBOM instead of writing it")
    args = parser.parse_args(argv)
    try:
        if args.check:
            if check_sbom(args.output):
                print("SBOM OK:", args.output)
                return 0
            print("SBOM MISMATCH or missing:", args.output, file=sys.stderr)
            return 2
        write_sbom(args.output)
        print("SBOM WRITTEN:", args.output)
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
