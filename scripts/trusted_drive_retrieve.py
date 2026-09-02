from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
import urllib.request
from pathlib import Path
from typing import Any


DRIVE_FILE_RE = re.compile(r"/file/d/([^/]+)")
DRIVE_FOLDER_RE = re.compile(r"/folders/([^/?]+)")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
MAX_LOGICAL_BYTES = 2 * 1024 * 1024 * 1024


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_safe_file_name(name: str) -> None:
    if not name or Path(name).name != name or "/" in name or "\\" in name or "\x00" in name:
        raise ValueError(f"unsafe file name: {name!r}")


def extract_locator_id(locator: str, kind: str) -> str:
    pattern = DRIVE_FILE_RE if kind == "GOOGLE_DRIVE_FILE" else DRIVE_FOLDER_RE
    match = pattern.search(locator)
    if not match:
        raise ValueError(f"request locator does not match {kind}")
    return match.group(1)


def download_drive_file(file_id: str, token: str, destination: Path, maximum_bytes: int) -> tuple[int, str]:
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&supportsAllDrives=true"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    digest = hashlib.sha256()
    total = 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as output:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            total += len(block)
            if total > maximum_bytes:
                raise ValueError(f"Drive object {file_id} exceeded declared size bound")
            digest.update(block)
            output.write(block)
    return total, digest.hexdigest()


def select_source(request: dict[str, Any], bundle: dict[str, Any]) -> dict[str, Any]:
    expected_sha = request["source"]["sha256"].lower()
    expected_name = request["source"]["file_name"]
    candidates = [
        source
        for source in bundle["sources"]
        if source["sha256"].lower() == expected_sha and source["file_name"] == expected_name
    ]
    if len(candidates) != 1:
        raise ValueError(f"request did not resolve to exactly one SourceBundle entry: {len(candidates)}")
    return candidates[0]


def verify_request(request: dict[str, Any]) -> None:
    source = request.get("source", {})
    profile = request.get("authorization_profile", {})
    if source.get("kind") != "GOOGLE_DRIVE":
        raise ValueError("trusted Drive retrieval accepts GOOGLE_DRIVE requests only")
    require_safe_file_name(source.get("file_name", ""))
    if not SHA256_RE.fullmatch(str(source.get("sha256", "")).lower()):
        raise ValueError("request source SHA-256 is invalid")
    if profile.get("static_analysis_allowed") is not True:
        raise ValueError("static analysis is not authorized")
    if request.get("requested_mode") not in {"INTERACTIVE_RESUMABLE", "UNATTENDED_AGENTIC", None}:
        raise ValueError("unsupported requested_mode")


def retrieve(request_path: Path, bundle_path: Path, package_dir: Path, record_path: Path) -> None:
    token = os.environ.get("GDRIVE_ACCESS_TOKEN", "")
    if not token:
        raise ValueError("GDRIVE_ACCESS_TOKEN is missing")

    request = load_json(request_path)
    bundle = load_json(bundle_path)
    verify_request(request)
    if bundle.get("authorization_state") != "AUTHORIZED":
        raise ValueError("SourceBundle is not authorized")
    source = select_source(request, bundle)
    storage = source["storage"]
    expected_sha = source["sha256"].lower()
    expected_size = int(source["size_bytes"])
    if expected_size <= 0 or expected_size > MAX_LOGICAL_BYTES:
        raise ValueError("logical package size is outside trusted intake bounds")

    package_dir.mkdir(parents=True, exist_ok=True)
    final_path = package_dir / source["file_name"]
    if final_path.exists():
        final_path.unlink()

    parts_record: list[dict[str, Any]] = []
    temporary_root = Path(tempfile.mkdtemp(prefix="appfusion-drive-parts-", dir=str(package_dir)))
    try:
        if storage["kind"] == "GOOGLE_DRIVE_FILE":
            request_id = extract_locator_id(request["source"]["locator"], "GOOGLE_DRIVE_FILE")
            if request_id != storage["drive_file_id"]:
                raise ValueError("request Drive file locator disagrees with SourceBundle")
            size, digest = download_drive_file(storage["drive_file_id"], token, final_path, expected_size)
            if size != expected_size or digest != expected_sha:
                raise ValueError("downloaded Drive file failed size/SHA-256 verification")
            parts_record.append({
                "sequence": 1,
                "drive_file_id": storage["drive_file_id"],
                "size_bytes": size,
                "sha256": digest,
            })
        elif storage["kind"] == "GOOGLE_DRIVE_CHUNKED":
            request_folder_id = extract_locator_id(request["source"]["locator"], "GOOGLE_DRIVE_CHUNKED")
            if request_folder_id != storage["drive_folder_id"]:
                raise ValueError("request Drive folder locator disagrees with SourceBundle")
            reconstruction = sorted(storage["reconstruction_order"], key=lambda item: item["sequence"])
            if [item["sequence"] for item in reconstruction] != list(range(1, len(reconstruction) + 1)):
                raise ValueError("chunk sequence is not contiguous from 1")
            with final_path.open("wb") as assembled:
                for part in reconstruction:
                    require_safe_file_name(part["file_name"])
                    part_path = temporary_root / f"{part['sequence']:04d}-{part['file_name']}"
                    declared_size = int(part["size_bytes"])
                    declared_sha = part["sha256"].lower()
                    size, digest = download_drive_file(part["drive_file_id"], token, part_path, declared_size)
                    if size != declared_size or digest != declared_sha:
                        raise ValueError(f"chunk {part['sequence']} failed size/SHA-256 verification")
                    with part_path.open("rb") as source_handle:
                        shutil.copyfileobj(source_handle, assembled, 1024 * 1024)
                    parts_record.append({
                        "sequence": part["sequence"],
                        "drive_file_id": part["drive_file_id"],
                        "size_bytes": size,
                        "sha256": digest,
                    })
            if final_path.stat().st_size != expected_size or sha256_file(final_path) != expected_sha:
                raise ValueError("reconstructed logical package failed size/SHA-256 verification")
        else:
            raise ValueError(f"unsupported storage kind: {storage['kind']}")

        record = {
            "schema_version": "1.0.0",
            "request_id": request["request_id"],
            "bundle_id": bundle["bundle_id"],
            "source_id": source["source_id"],
            "artifact_format": source["artifact_format"],
            "file_name": source["file_name"],
            "verified_sha256": expected_sha,
            "verified_size_bytes": expected_size,
            "storage_kind": storage["kind"],
            "parts": parts_record,
            "authorization_profile_id": request["authorization_profile"]["profile_id"],
            "static_analysis_allowed": True,
            "network_interception_allowed": request["authorization_profile"]["network_interception_allowed"],
        }
        record_path.parent.mkdir(parents=True, exist_ok=True)
        record_path.write_text(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"VERIFIED_SOURCE_ID={source['source_id']}")
        print(f"VERIFIED_SHA256={expected_sha}")
        print(f"VERIFIED_SIZE_BYTES={expected_size}")
    except Exception:
        if final_path.exists():
            final_path.unlink()
        raise
    finally:
        shutil.rmtree(temporary_root, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request_path", type=Path)
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("package_dir", type=Path)
    parser.add_argument("record_path", type=Path)
    args = parser.parse_args()
    retrieve(args.request_path, args.bundle_path, args.package_dir, args.record_path)


if __name__ == "__main__":
    main()
