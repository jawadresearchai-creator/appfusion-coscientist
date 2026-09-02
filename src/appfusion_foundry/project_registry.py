from __future__ import annotations

from typing import Any


def select_application(registry: dict[str, Any]) -> dict[str, Any]:
    """Return the deterministic new-session application-selection decision."""

    active = [
        application
        for application in registry.get("applications", [])
        if application.get("active_for_selection") is True
    ]
    active.sort(key=lambda item: (item["display_name"].casefold(), item["app_id"]))
    candidates = [item["app_id"] for item in active]

    if not active:
        return {
            "selection_decision": "NO_ACTIVE_APPLICATIONS",
            "selected_app_id": None,
            "candidate_app_ids": [],
        }
    if len(active) == 1:
        return {
            "selection_decision": "AUTO_SELECTED",
            "selected_app_id": active[0]["app_id"],
            "candidate_app_ids": candidates,
        }
    return {
        "selection_decision": "USER_SELECTION_REQUIRED",
        "selected_app_id": None,
        "candidate_app_ids": candidates,
    }
