from __future__ import annotations

import copy
import json
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .contracts import load_json, validate


APP_STREAM_NAMESPACE = uuid.UUID("8325d876-675b-4de7-95a9-ebf35282defc")


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def utc_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class LeaseHandle:
    path: Path
    token: str
    holder_id: str

    def release(self) -> None:
        if not self.path.exists():
            return
        current = json.loads(self.path.read_text(encoding="utf-8"))
        if current.get("lease_token") != self.token:
            raise RuntimeError("Lease ownership changed; refusing to remove another writer's lease")
        self.path.unlink()


def acquire_file_lease(
    lease_root: Path,
    app_id: str,
    holder_id: str,
    *,
    now: datetime | None = None,
    ttl: timedelta = timedelta(minutes=20),
) -> LeaseHandle:
    """Acquire an optional/local adapter lease with exclusive file creation.

    Canonical Git promotion still relies on fast-forward conflict rejection. This
    adapter prevents two workers sharing one filesystem from preparing the same
    application transition concurrently.
    """

    if re.fullmatch(r"[a-z0-9][a-z0-9-]{2,63}", app_id) is None:
        raise ValueError("Invalid application identifier")
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    if ttl <= timedelta(0):
        raise ValueError("Lease TTL must be positive")
    lease_root.mkdir(parents=True, exist_ok=True)
    path = lease_root / f"{app_id}.json"
    token = str(uuid.uuid4())
    payload = {
        "schema_version": "1.0.0",
        "app_id": app_id,
        "holder_id": holder_id,
        "lease_token": token,
        "acquired_at": utc_text(now),
        "expires_at": utc_text(now + ttl),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"

    while True:
        try:
            descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if parse_utc(existing["expires_at"]) > now:
                raise RuntimeError(
                    f"Application {app_id} is leased by {existing['holder_id']} until {existing['expires_at']}"
                )
            stale = path.with_name(f"{path.stem}.expired-{existing['lease_token']}.json")
            try:
                os.replace(path, stale)
            except FileNotFoundError:
                continue
            continue
        else:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            return LeaseHandle(path=path, token=token, holder_id=holder_id)


def plan_transition(
    registry: dict[str, Any],
    application: dict[str, Any],
    transition: dict[str, Any],
    previous_event_id: str | None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if transition["app_id"] != application["app_id"]:
        raise ValueError("Transition application does not match ApplicationState")
    if transition["expected_registry_revision"] != registry["registry_revision"]:
        raise ValueError("STALE_REGISTRY_REVISION")
    if transition["expected_application_state_revision"] != application["state_revision"]:
        raise ValueError("STALE_APPLICATION_STATE_REVISION")
    if transition["event_sequence"] != application["last_event_sequence"] + 1:
        raise ValueError("NON_CONTIGUOUS_EVENT_SEQUENCE")

    updated_application = copy.deepcopy(application)
    updated_application.update(
        {
            "schema_version": "1.1.0",
            "lifecycle_state": transition["next_lifecycle_state"],
            "phase": transition["next_phase"],
            "updated_at": transition["occurred_at"],
            "state_revision": application["state_revision"] + 1,
            "last_event_sequence": transition["event_sequence"],
            "delivery_plan_id": transition["delivery_plan_id"],
            "last_completed_event": {
                "event_type": transition["event_type"],
                "occurred_at": transition["occurred_at"],
                "summary": transition["event_summary"],
            },
            "next_safe_action": transition["next_safe_action"],
        }
    )

    updated_registry = copy.deepcopy(registry)
    updated_registry["schema_version"] = "1.1.0"
    updated_registry["registry_revision"] += 1
    updated_registry["updated_at"] = transition["occurred_at"]
    matches = [index for index, item in enumerate(updated_registry["applications"]) if item["app_id"] == application["app_id"]]
    if len(matches) != 1:
        raise ValueError("Registry must contain exactly one matching application")
    updated_registry["applications"][matches[0]] = copy.deepcopy(updated_application)
    updated_registry["system"].update(
        {
            "status": "READY" if transition["next_lifecycle_state"] not in {"PAUSED", "FAILED"} else transition["next_lifecycle_state"],
            "phase": transition["next_lifecycle_state"],
            "current_milestone": transition["event_type"],
            "last_completed_event": {
                "event_type": transition["event_type"],
                "occurred_at": transition["occurred_at"],
                "summary": transition["event_summary"],
            },
            "next_safe_action": transition["next_safe_action"],
            "blockers": copy.deepcopy(updated_application["blockers"]),
        }
    )

    stream_run_id = str(uuid.uuid5(APP_STREAM_NAMESPACE, transition["app_id"]))
    event = {
        "schema_version": "1.1.0",
        "event_id": transition["transition_id"],
        "run_id": stream_run_id,
        "sequence": transition["event_sequence"],
        "event_type": transition["event_type"],
        "occurred_at": transition["occurred_at"],
        "actor": transition["actor"],
        "stream_id": transition["app_id"],
        "previous_event_id": previous_event_id,
        "idempotency_key": transition["transition_id"],
        "payload": {
            "app_id": transition["app_id"],
            "registry_revision_before": transition["expected_registry_revision"],
            "registry_revision_after": updated_registry["registry_revision"],
            "application_state_revision_before": transition["expected_application_state_revision"],
            "application_state_revision_after": updated_application["state_revision"],
            "delivery_plan_id": transition["delivery_plan_id"],
            "evidence": transition.get("evidence", []),
        },
    }
    return updated_registry, updated_application, event


def evaluate_release_readiness(plan: dict[str, Any], *, evaluated_at: str) -> dict[str, Any]:
    required_journeys = set(plan["terminal_condition"]["required_journey_ids"])
    passed_journeys = {item["journey_id"] for item in plan["user_journeys"] if item["status"] == "PASS"}
    required_artifacts = set(plan["terminal_condition"]["required_artifact_kinds"])
    passed_artifacts = {
        item["artifact_kind"]
        for item in plan["deliverables"]
        if item["required_for_train"] and item["status"] == "PASS"
    }
    journeys_pass = required_journeys <= passed_journeys
    artifacts_pass = required_artifacts <= passed_artifacts
    open_critical_defects = [
        item["defect_id"]
        for item in plan["defects"]
        if item["severity"] == "CRITICAL" and item["status"] == "OPEN"
    ]
    critical_clear = not open_critical_defects
    reasons: list[str] = []
    if not journeys_pass:
        reasons.append("Required journeys are incomplete: " + ", ".join(sorted(required_journeys - passed_journeys)))
    if not artifacts_pass:
        reasons.append("Required artifacts are incomplete: " + ", ".join(sorted(required_artifacts - passed_artifacts)))
    if not critical_clear:
        reasons.append("Open critical defects: " + ", ".join(sorted(open_critical_defects)))
    return {
        "schema_version": "1.0.0",
        "app_id": plan["app_id"],
        "plan_id": plan["plan_id"],
        "evaluated_at": evaluated_at,
        "required_journeys_pass": journeys_pass,
        "required_artifacts_pass": artifacts_pass,
        "zero_critical_defects": critical_clear,
        "ready": journeys_pass and artifacts_pass and critical_clear,
        "reasons": reasons,
    }


def validate_control_state(repository_root: Path) -> list[str]:
    errors: list[str] = []
    schema_root = repository_root / "schemas" / "v1"
    registry = load_json(repository_root / "state" / "APPFUSION_PROJECT_REGISTRY.json")
    try:
        validate(registry, schema_root / "project-registry.schema.json")
    except Exception as exc:
        errors.append(f"Registry validation failed: {exc}")
        return errors

    event_paths = sorted((repository_root / "state" / "events").glob("*.json"))
    events = []
    for path in event_paths:
        try:
            event = load_json(path)
            validate(event, schema_root / "run-event.schema.json")
            events.append(event)
        except Exception as exc:
            errors.append(f"Event {path.name} failed validation: {exc}")
    by_sequence = {event["sequence"]: event for event in events}
    if len(by_sequence) != len(events):
        errors.append("Event sequences are not unique")

    for embedded in registry["applications"]:
        app_path = repository_root / "state" / "applications" / f"{embedded['app_id']}.json"
        if not app_path.exists():
            errors.append(f"Missing ApplicationState file for {embedded['app_id']}")
            continue
        application = load_json(app_path)
        try:
            validate(application, schema_root / "application-state.schema.json")
        except Exception as exc:
            errors.append(f"ApplicationState {embedded['app_id']} failed validation: {exc}")
            continue
        if application != embedded:
            errors.append(f"Registry projection differs from ApplicationState for {embedded['app_id']}")
        if application.get("schema_version") == "1.1.0":
            if registry["registry_revision"] != application["state_revision"]:
                errors.append(
                    f"Registry revision {registry['registry_revision']} differs from "
                    f"ApplicationState revision {application['state_revision']} for {embedded['app_id']}"
                )
            tail = application["last_event_sequence"]
            if tail not in by_sequence:
                errors.append(f"Application {embedded['app_id']} event tail {tail} is missing")
            start = min(by_sequence) if by_sequence else tail
            missing = [sequence for sequence in range(start, tail + 1) if sequence not in by_sequence]
            if missing:
                errors.append(f"Application {embedded['app_id']} has missing event sequences: {missing}")
            tail_event = by_sequence.get(tail)
            if tail_event and tail_event.get("payload", {}).get("app_id") != embedded["app_id"]:
                errors.append(f"Application {embedded['app_id']} event tail belongs to a different application")
            chained_events = [event for event in events if event.get("schema_version") == "1.1.0"]
            seen_idempotency_keys: set[str] = set()
            for event in chained_events:
                key = event["idempotency_key"]
                if key in seen_idempotency_keys:
                    errors.append(f"Duplicate event idempotency key: {key}")
                seen_idempotency_keys.add(key)
                predecessor = by_sequence.get(event["sequence"] - 1)
                if predecessor and event["previous_event_id"] != predecessor["event_id"]:
                    errors.append(f"Event {event['sequence']} does not chain to event {event['sequence'] - 1}")
            plan_id = application["delivery_plan_id"]
            plan_path = repository_root / "state" / "delivery-plans" / f"{plan_id}.json"
            if not plan_path.exists():
                errors.append(f"Application {embedded['app_id']} delivery plan is missing: {plan_id}")
            else:
                try:
                    plan = load_json(plan_path)
                    validate(plan, schema_root / "delivery-plan.schema.json")
                    if plan["app_id"] != embedded["app_id"]:
                        errors.append(f"Delivery plan {plan_id} belongs to a different application")
                except Exception as exc:
                    errors.append(f"Delivery plan {plan_id} failed validation: {exc}")
    return errors
