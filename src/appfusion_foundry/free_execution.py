"""Free-only admission: evaluate verified provider evidence before dispatch.

This does not discover billing state or switch billing off. Evidence must come
from the provider/account UI or authenticated API, not from an agent's guess.
Provider-side billing disabled/hard stop is the actual financial boundary.
"""
from datetime import datetime, timedelta, timezone
from typing import Any


def admit_free_execution(evidence: dict[str, Any], *, now: datetime) -> list[str]:
    errors = []
    required = {
        "access_authorized": True,
        "billing_enabled": False,
        "overage_enabled": False,
        "hard_stop_at_free_limit": True,
    }
    for field, expected in required.items():
        if evidence.get(field) is not expected:
            errors.append(f"{field} must be verified as {expected}")
    if type(evidence.get("maximum_new_charge")) not in (int, float) or evidence["maximum_new_charge"] != 0:
        errors.append("Maximum new charge must be exactly zero")
    if not evidence.get("provider_evidence_ref"):
        errors.append("Provider/account evidence reference is required")
    try:
        verified = datetime.fromisoformat(evidence["verified_at"].replace("Z", "+00:00"))
        if verified.tzinfo is None or now.tzinfo is None:
            raise ValueError("Timezone required")
        age = now.astimezone(timezone.utc) - verified.astimezone(timezone.utc)
        if not timedelta(0) <= age <= timedelta(hours=1):
            errors.append("Free allowance evidence is stale or future-dated")
    except (KeyError, TypeError, ValueError):
        errors.append("Valid verification timestamp is required")
    provider = evidence.get("provider")
    if provider == "OPTIONAL_LOCAL":
        if evidence.get("existing_authorized_hardware") is not True:
            errors.append("Local hardware must already exist and be authorized")
    elif provider == "GITHUB_PUBLIC_STANDARD":
        for field in ("max_job_minutes",):
            value = evidence.get(field)
            if type(value) not in (int, float) or not 0 <= value < float("inf"):
                errors.append(f"Finite nonnegative {field} is required")
        if not errors and evidence["max_job_minutes"] <= 0:
            errors.append("Job must have a positive bounded timeout")
        if evidence.get("repository_visibility") != "public" or evidence.get("publication_authorized") is not True:
            errors.append("Public Product source requires explicit publication authorization")
        if evidence.get("standard_runner") is not True or evidence.get("monthly_compute_quota") is not False:
            errors.append("Only verified quota-independent standard public runners are admitted")
        if evidence.get("private_source_proxy") is not False:
            errors.append("Public runners cannot be a disguised private-source CI proxy")
    else:
        errors.append("Unknown provider: cost and eligibility not established")
    return errors
