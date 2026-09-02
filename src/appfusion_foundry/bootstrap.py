from __future__ import annotations

import json
from pathlib import Path

import yaml

from .contracts import REQUIRED_SCHEMA_NAMES, STAGE_OUTCOMES, load_json, schema_catalog


FORBIDDEN_CANONICAL_TOKENS = ("E:\\\\", "C:\\\\Users\\", "/Users/", "/home/")


def bootstrap_check(repository_root: Path) -> list[str]:
    errors: list[str] = []
    schema_root = repository_root / "schemas" / "v1"
    try:
        catalog = schema_catalog(schema_root)
    except Exception as exc:
        return [str(exc)]
    missing = sorted(REQUIRED_SCHEMA_NAMES - set(catalog))
    if missing:
        errors.append(f"Missing required schemas: {', '.join(missing)}")

    outcome_schema = load_json(catalog["StageOutcome"])
    declared = set(outcome_schema["properties"]["outcome"]["enum"])
    if declared != STAGE_OUTCOMES:
        errors.append("StageOutcome enum does not match the canonical outcome set")
    if "FAILED_BLOCKED_ENVIRONMENT" in declared:
        errors.append("Deprecated contradictory outcome FAILED_BLOCKED_ENVIRONMENT is present")

    profile_path = repository_root / "policies" / "untrusted-runner-profile.yaml"
    profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    if profile.get("github_token_permissions") != {}:
        errors.append("Untrusted runner must declare empty GitHub token permissions")
    if profile.get("persist_checkout_credentials") is not False:
        errors.append("Untrusted runner must disable checkout credential persistence")

    scan_roots = [repository_root / "policies", repository_root / ".github" / "workflows"]
    for root in scan_roots:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for token in FORBIDDEN_CANONICAL_TOKENS:
                if token in text:
                    errors.append(f"Required local path token {token!r} found in {path.relative_to(repository_root)}")

    manifest = json.loads((repository_root / "environment-manifest.json").read_text(encoding="utf-8"))
    if manifest.get("local_environment", {}).get("role") != "OPTIONAL_ADAPTER":
        errors.append("Local environment is not explicitly optional")
    if manifest.get("canonical_state", {}).get("authority") != "CLOUD":
        errors.append("Cloud is not declared as canonical authority")
    return errors
