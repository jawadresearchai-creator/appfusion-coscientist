from __future__ import annotations

import json
import zipfile
from pathlib import Path

from .contracts import file_sha256


def inventory_apk(apk_path: Path) -> dict[str, object]:
    if apk_path.suffix.lower() != ".apk":
        raise ValueError("FOUNDRY_VERTICAL_SLICE_ALPHA accepts .apk only")
    if not zipfile.is_zipfile(apk_path):
        raise ValueError("Input is not a valid ZIP-structured APK")
    with zipfile.ZipFile(apk_path) as archive:
        names = sorted(archive.namelist())
    return {
        "schema_version": "1.0.0",
        "file_name": apk_path.name,
        "sha256": file_sha256(apk_path),
        "size_bytes": apk_path.stat().st_size,
        "entry_count": len(names),
        "has_android_manifest": "AndroidManifest.xml" in names,
        "dex_files": [name for name in names if name.startswith("classes") and name.endswith(".dex")],
        "native_libraries": [name for name in names if name.startswith("lib/") and name.endswith(".so")],
        "resource_archives": [name for name in names if name == "resources.arsc"],
    }


def write_inventory(apk_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(inventory_apk(apk_path), indent=2) + "\n", encoding="utf-8")
