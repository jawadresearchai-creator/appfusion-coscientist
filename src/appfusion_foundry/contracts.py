from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


STAGE_OUTCOMES = frozenset(
    {
        "PASS",
        "FAIL",
        "SKIPPED_NOT_APPLICABLE",
        "SKIPPED_POLICY",
        "BLOCKED_AUTHORIZATION",
        "BLOCKED_ENVIRONMENT",
        "BLOCKED_SECURITY_ENVIRONMENT",
        "BLOCKED_BUDGET",
        "INCONCLUSIVE",
        "CANCELLED",
    }
)

PAUSED_STATES = frozenset(
    {
        "PAUSED_MODEL_CAPACITY",
        "PAUSED_REASONING_RUNTIME",
        "PAUSED_CI_BUDGET",
        "PAUSED_AUTHORIZATION",
        "PAUSED_BLUEPRINT_REVOKED",
        "PAUSED_USER_INTERVENTION",
    }
)

REQUIRED_SCHEMA_NAMES = frozenset(
    {
        "AnalysisAuthorizationProfile",
        "ApprovalEnvelope",
        "ApprovalEvent",
        "FoundryDecisionDossier",
        "IntakeRequest",
        "ProductApprovalAttestation",
        "ProductBlueprint",
        "ProductEngineCandidate",
        "ProductEngineFeasibilityRecord",
        "RunStateSnapshot",
        "RunEvent",
        "EvidenceDependency",
        "CleanRoomTransferManifest",
        "FirstModuleCheckpoint",
        "EnvironmentSnapshot",
        "ArtifactRecord",
        "BudgetAuthorization",
        "ModelInvocation",
        "SecurityFinding",
        "LicenseDecision",
        "ReleaseSignerRecord",
        "FoundryEvaluationProtocol",
        "FoundryEvaluationResult",
        "StageOutcome",
        "UntrustedRunnerProfile",
        "ApplicationState",
        "ProjectRegistry",
        "SessionBootstrap",
        "SourceBundle",
    }
)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def validate(instance: Any, schema_path: Path) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    registry = Registry()
    for candidate in schema_path.parent.glob("*.schema.json"):
        referenced = load_json(candidate)
        if "$id" in referenced:
            registry = registry.with_resource(referenced["$id"], Resource.from_contents(referenced))
    Draft202012Validator(schema, registry=registry).validate(instance)


def schema_catalog(schema_root: Path) -> dict[str, Path]:
    catalog: dict[str, Path] = {}
    for path in sorted(schema_root.glob("*.schema.json")):
        schema = load_json(path)
        title = schema.get("title")
        if not isinstance(title, str) or not title:
            raise ValueError(f"Schema has no title: {path}")
        if title in catalog:
            raise ValueError(f"Duplicate schema title: {title}")
        catalog[title] = path
    return catalog
