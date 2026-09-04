from datetime import datetime, timezone
import json

import pytest
from jsonschema import ValidationError

from appfusion_foundry.contracts import validate
from appfusion_foundry.free_execution import admit_free_execution
from test_bootstrap import ROOT

NOW = datetime(2026, 9, 4, 3, tzinfo=timezone.utc)


def valid_evidence():
    return dict(provider="GITHUB_PUBLIC_STANDARD", repository_visibility="public", publication_authorized=True,
                standard_runner=True, monthly_compute_quota=False, private_source_proxy=False,
                access_authorized=True, billing_enabled=False, overage_enabled=False,
                hard_stop_at_free_limit=True, maximum_new_charge=0,
                provider_evidence_ref="fixture-account-readback", verified_at=NOW.isoformat(),
                max_job_minutes=30)


def test_explicitly_authorized_standard_public_runner_admitted():
    assert admit_free_execution(valid_evidence(), now=NOW) == []


@pytest.mark.parametrize("field,value", [
    ("billing_enabled", True), ("overage_enabled", True), ("access_authorized", False),
    ("hard_stop_at_free_limit", False), ("maximum_new_charge", 1),
    ("provider_evidence_ref", ""), ("verified_at", "2026-09-03T00:00:00Z"),
    ("verified_at", "2026-09-05T00:00:00Z"), ("verified_at", "invalid"),
    ("publication_authorized", False), ("max_job_minutes", 0),
    ("max_job_minutes", -1), ("repository_visibility", "private"), ("standard_runner", False),
    ("monthly_compute_quota", True), ("private_source_proxy", True), ("provider", "CODEMAGIC"),
    ("provider", "UNVERIFIED_PROVIDER"), ("max_job_minutes", float("nan")),
])
def test_charge_unknown_expired_or_ineligible_denied(field, value):
    evidence = valid_evidence()
    evidence[field] = value
    assert admit_free_execution(evidence, now=NOW)


def test_missing_fields_fail_closed():
    assert admit_free_execution({}, now=NOW)


def test_optional_local_route_requires_existing_authorized_hardware():
    evidence = valid_evidence() | {"provider": "OPTIONAL_LOCAL", "existing_authorized_hardware": True}
    assert admit_free_execution(evidence, now=NOW) == []
    evidence["existing_authorized_hardware"] = False
    assert admit_free_execution(evidence, now=NOW)


def test_budget_contract_cannot_authorize_paid_work():
    base = {"schema_version": "1.0.0", "budget_class": "CI_COMPUTE", "paid_overage_authorized": False}
    schema = ROOT / "schemas/v1/budget-authorization.schema.json"
    validate(base, schema)
    for patch in ({"paid_overage_authorized": True}, {"per_run_cap": 1}, {"cumulative_cap": 1}):
        with pytest.raises(ValidationError):
            validate(base | patch, schema)


def test_active_product_routes_to_authorized_public_repo_without_local_dependency():
    manifest = json.loads((ROOT / "environment-manifest.json").read_text())
    application = json.loads((ROOT / "state/applications/docvault-lasttime-fusion.json").read_text())
    repositories = manifest["canonical_state"]["repositories"]
    assert repositories["product_foundry"] == "jawadresearchai-creator/appfusion-product-public"
    assert application["artifact_locations"]["product_repository"] == repositories["product_foundry"]
    assert repositories["historical_private_product"] == "jawadresearchai-creator/appfusion-product"
    assert manifest["local_environment"]["required_for_operation"] is False
    assert manifest["budgets"]["paid_overage_authorized"] is False
    assert manifest["budgets"]["standard_runner_allowlist"] == ["ubuntu-24.04", "macos-15"]
