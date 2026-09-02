from __future__ import annotations

import json
import re
import sys
from pathlib import PurePosixPath

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_KEYS = {
    "schema_version",
    "container_kind",
    "file_name",
    "sha256",
    "size_bytes",
    "entry_count",
    "total_uncompressed_bytes",
    "has_android_manifest",
    "dex_files",
    "native_libraries",
    "resource_archives",
    "nested_apks",
}


def safe_name(value: str) -> bool:
    if not value or len(value.encode("utf-8")) > 1024 or "\\" in value or "\x00" in value:
        return False
    if value.startswith("/") or (len(value) > 1 and value[1] == ":"):
        return False
    trimmed = value[:-1] if value.endswith("/") else value
    parts = PurePosixPath(trimmed).parts
    return all(part not in {"", ".", ".."} for part in parts)


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    if len(sys.argv) != 4:
        fail("usage: validate_static_inventory.py <inventory.json> <expected_sha256> <expected_size>")
    payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
    expected_sha256 = sys.argv[2].lower()
    expected_size = int(sys.argv[3])

    if set(payload) != ALLOWED_KEYS:
        fail(f"unexpected inventory fields: {sorted(set(payload) ^ ALLOWED_KEYS)}")
    if payload["schema_version"] != "1.0.0":
        fail("invalid schema_version")
    if payload["container_kind"] not in {"APK", "APKM", "XAPK"}:
        fail("invalid container_kind")
    if not safe_name(payload["file_name"]):
        fail("unsafe file_name")
    if not SHA256_RE.fullmatch(payload["sha256"]):
        fail("invalid sha256")
    if payload["sha256"] != expected_sha256:
        fail("input sha256 mismatch")
    if payload["size_bytes"] != expected_size or payload["size_bytes"] <= 0:
        fail("input size mismatch")
    if not isinstance(payload["entry_count"], int) or not 1 <= payload["entry_count"] <= 200000:
        fail("invalid entry_count")
    if not isinstance(payload["total_uncompressed_bytes"], int) or not 0 <= payload["total_uncompressed_bytes"] <= 8 * 1024**3:
        fail("invalid total_uncompressed_bytes")
    if not isinstance(payload["has_android_manifest"], bool):
        fail("invalid has_android_manifest")

    for key in ("dex_files", "native_libraries", "resource_archives", "nested_apks"):
        values = payload[key]
        if not isinstance(values, list) or len(values) > 10000:
            fail(f"invalid {key}")
        if not all(isinstance(value, str) and safe_name(value) for value in values):
            fail(f"unsafe value in {key}")

    print("STATIC_INVENTORY_VALIDATED")


if __name__ == "__main__":
    main()
