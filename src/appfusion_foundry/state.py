from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .contracts import canonical_sha256


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def create_run(request: dict[str, Any], output_root: Path) -> Path:
    run_id = str(uuid.uuid4())
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    request_hash = canonical_sha256(request)
    event = {
        "schema_version": "1.0.0",
        "event_id": str(uuid.uuid4()),
        "run_id": run_id,
        "sequence": 1,
        "event_type": "RUN_REGISTERED",
        "occurred_at": utc_now(),
        "actor": os.environ.get("GITHUB_ACTOR", "optional-local-adapter"),
        "payload": {"intake_request_sha256": request_hash},
    }
    (run_dir / "intake-request.json").write_text(
        json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (run_dir / "events.jsonl").write_text(
        json.dumps(event, sort_keys=True) + "\n", encoding="utf-8"
    )
    return run_dir
