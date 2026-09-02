from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .contracts import canonical_sha256


APPFUSION_RUN_NAMESPACE = uuid.UUID("b90e77bb-44f6-4e5c-a7b5-25f38a74686d")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def create_run(request: dict[str, Any], output_root: Path) -> Path:
    run_id = str(uuid.uuid5(APPFUSION_RUN_NAMESPACE, request["request_id"]))
    run_dir = output_root / run_id
    request_hash = canonical_sha256(request)
    event_id = str(uuid.uuid5(APPFUSION_RUN_NAMESPACE, f"{run_id}:1:RUN_REGISTERED"))
    event = {
        "schema_version": "1.0.0",
        "event_id": event_id,
        "run_id": run_id,
        "sequence": 1,
        "event_type": "RUN_REGISTERED",
        "occurred_at": request["submitted_at"],
        "actor": request["submitted_by"],
        "payload": {"intake_request_sha256": request_hash},
    }
    request_text = json.dumps(request, indent=2, sort_keys=True) + "\n"
    event_text = json.dumps(event, sort_keys=True) + "\n"
    if run_dir.exists():
        if (run_dir / "intake-request.json").read_text(encoding="utf-8") != request_text:
            raise ValueError(f"Run ID collision or mutated request: {run_id}")
        if (run_dir / "events.jsonl").read_text(encoding="utf-8") != event_text:
            raise ValueError(f"Run registration event changed: {run_id}")
        return run_dir
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "intake-request.json").write_text(
        request_text, encoding="utf-8"
    )
    (run_dir / "events.jsonl").write_text(
        event_text, encoding="utf-8"
    )
    return run_dir
