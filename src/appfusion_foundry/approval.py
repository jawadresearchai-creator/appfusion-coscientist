from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from .contracts import canonical_sha256, load_json
from .state import utc_now


def policy_bundle_hash(policy_root: Path) -> str:
    bundle = []
    for path in sorted(item for item in policy_root.rglob("*") if item.is_file()):
        bundle.append({"path": path.relative_to(policy_root).as_posix(), "content": path.read_text(encoding="utf-8")})
    return canonical_sha256(bundle)


def create_approval_artifacts(
    dossier: dict[str, Any],
    blueprint: dict[str, Any],
    approver_principal: str,
    policy_hash: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    approval_id = str(uuid.uuid4())
    approved_at = utc_now()
    blueprint_hash = canonical_sha256(blueprint)
    envelope = {
        "schema_version": "1.0.0",
        "approval_id": approval_id,
        "foundry_dossier_sha256": canonical_sha256(dossier),
        "product_blueprint_sha256": blueprint_hash,
        "approver_principal": approver_principal,
        "approved_at": approved_at,
        "policy_bundle_hash": policy_hash,
        "clean_room_schema_version": blueprint["schema_version"],
        "approval_status": "APPROVED",
        "conditions": [],
    }
    attestation = {
        "schema_version": "1.0.0",
        "approval_id": approval_id,
        "product_blueprint_sha256": blueprint_hash,
        "approval_status": "APPROVED",
        "approved_at": approved_at,
        "policy_bundle_hash": policy_hash,
        "clean_room_schema_version": blueprint["schema_version"],
        "conditions": [],
    }
    return envelope, attestation


def write_approval_artifacts(
    dossier_path: Path,
    blueprint_path: Path,
    approver_principal: str,
    policy_root: Path,
    output_root: Path,
) -> tuple[Path, Path]:
    dossier = load_json(dossier_path)
    blueprint = load_json(blueprint_path)
    envelope, attestation = create_approval_artifacts(
        dossier,
        blueprint,
        approver_principal,
        policy_bundle_hash(policy_root),
    )
    output_root.mkdir(parents=True, exist_ok=False)
    envelope_path = output_root / "approval-envelope.json"
    attestation_path = output_root / "product-approval-attestation.json"
    envelope_path.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    attestation_path.write_text(json.dumps(attestation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return envelope_path, attestation_path
