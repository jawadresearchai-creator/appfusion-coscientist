import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pytest
from jsonschema import ValidationError

from appfusion_foundry.bootstrap import bootstrap_check
from appfusion_foundry.approval import create_approval_artifacts
from appfusion_foundry.contracts import STAGE_OUTCOMES, load_json, validate
from appfusion_foundry.state import create_run
from appfusion_foundry.static_inventory import inventory_apk
from appfusion_foundry.project_registry import select_application
from appfusion_foundry.orchestration import (
    acquire_file_lease,
    evaluate_release_readiness,
    plan_transition,
    validate_control_state,
)


ROOT = Path(__file__).resolve().parents[1]


def test_bootstrap_contracts_are_consistent():
    assert bootstrap_check(ROOT) == []


def test_declared_stage_outcomes_are_exact():
    schema = load_json(ROOT / "schemas/v1/stage-outcome.schema.json")
    assert set(schema["properties"]["outcome"]["enum"]) == STAGE_OUTCOMES


def test_intake_request_contract(tmp_path):
    request = {
        "schema_version": "1.0.0",
        "request_id": "973fdfee-20b4-43be-b3a9-d4912813b549",
        "submitted_by": "authenticated-user",
        "submitted_at": "2026-09-02T00:00:00Z",
        "source": {
            "kind": "GOOGLE_DRIVE",
            "locator": "drive-file-id",
            "sha256": "a" * 64,
            "file_name": "sample.apk",
        },
        "authorization_profile": {
            "profile_id": "41d18b20-f3f3-449a-91e4-ce14e68d69a0",
            "rights_basis": "OWNER",
            "static_analysis_allowed": True,
            "dynamic_analysis_allowed": False,
            "network_interception_allowed": False,
            "accepted_by": "authenticated-user",
            "accepted_at": "2026-09-02T00:00:00Z",
            "constraints": [],
        },
        "requested_mode": "INTERACTIVE_RESUMABLE",
    }
    validate(request, ROOT / "schemas/v1/intake-request.schema.json")

    apk = tmp_path / "sample.apk"
    with zipfile.ZipFile(apk, "w") as archive:
        archive.writestr("AndroidManifest.xml", b"fixture")
        archive.writestr("classes.dex", b"fixture")
    inventory = inventory_apk(apk)
    assert inventory["has_android_manifest"] is True
    assert inventory["dex_files"] == ["classes.dex"]


def test_cloud_is_authoritative_and_local_is_optional():
    manifest = json.loads((ROOT / "environment-manifest.json").read_text(encoding="utf-8"))
    assert manifest["canonical_state"]["authority"] == "CLOUD"
    assert manifest["local_environment"]["required_for_operation"] is False


def test_project_registry_is_valid_and_auto_selects_the_staged_product():
    registry = load_json(ROOT / "state/APPFUSION_PROJECT_REGISTRY.json")
    validate(registry, ROOT / "schemas/v1/project-registry.schema.json")
    assert select_application(registry) == {
        "selection_decision": "AUTO_SELECTED",
        "selected_app_id": "docvault-lasttime-fusion",
        "candidate_app_ids": ["docvault-lasttime-fusion"],
    }
    application_state = load_json(ROOT / "state/applications/docvault-lasttime-fusion.json")
    validate(application_state, ROOT / "schemas/v1/application-state.schema.json")


def test_delivery_control_state_is_contiguous_and_consistent():
    assert validate_control_state(ROOT) == []


def test_schema_format_checker_rejects_invalid_uuid():
    event = load_json(ROOT / "state/events/018-delivery-orchestration-v1-1-locked.json")
    event["event_id"] = "not-a-uuid"
    with pytest.raises(ValidationError):
        validate(event, ROOT / "schemas/v1/run-event.schema.json")


def test_file_lease_prevents_concurrent_local_writers(tmp_path):
    now = datetime(2026, 9, 3, 10, 40, 55, tzinfo=timezone.utc)
    first = acquire_file_lease(tmp_path, "docvault-lasttime-fusion", "worker-a", now=now)
    with pytest.raises(RuntimeError, match="leased by worker-a"):
        acquire_file_lease(tmp_path, "docvault-lasttime-fusion", "worker-b", now=now)
    first.release()
    second = acquire_file_lease(tmp_path, "docvault-lasttime-fusion", "worker-b", now=now)
    second.release()


def test_transition_rejects_stale_state_and_updates_both_projections():
    registry = load_json(ROOT / "state/APPFUSION_PROJECT_REGISTRY.json")
    application = load_json(ROOT / "state/applications/docvault-lasttime-fusion.json")
    transition = {
        "schema_version": "1.0.0",
        "transition_id": "50a09dcf-bdfc-461f-a052-d61f16860c67",
        "app_id": application["app_id"],
        "holder_id": "test-worker",
        "lease_token": "a456836a-c451-4a44-8aa3-77b45bf297f0",
        "expected_registry_revision": registry["registry_revision"],
        "expected_application_state_revision": application["state_revision"],
        "event_sequence": application["last_event_sequence"] + 1,
        "event_type": "INSTALLABLE_SHELL_STARTED",
        "event_summary": "The installable shell delivery slice started.",
        "occurred_at": "2026-09-03T11:00:00Z",
        "actor": "appfusion-coscientist",
        "next_lifecycle_state": "PRODUCT_CONSTRUCTION",
        "next_phase": "INSTALLABLE_SHELL_IN_PROGRESS",
        "next_safe_action": "Build and install the Android debug APK.",
        "delivery_plan_id": application["delivery_plan_id"],
        "evidence": ["state/delivery-plans/docvault-lasttime-fusion-v0.1.json"],
    }
    validate(transition, ROOT / "schemas/v1/state-transition-envelope.schema.json")
    updated_registry, updated_application, event = plan_transition(
        registry,
        application,
        transition,
        "91f0cc70-5a22-49c3-ac17-7c848146a21b",
    )
    assert updated_registry["registry_revision"] == registry["registry_revision"] + 1
    assert updated_application["state_revision"] == application["state_revision"] + 1
    assert updated_registry["applications"][0] == updated_application
    assert updated_registry["system"]["current_milestone"] == "INSTALLABLE_SHELL_STARTED"
    assert event["previous_event_id"] == "91f0cc70-5a22-49c3-ac17-7c848146a21b"

    transition["expected_registry_revision"] = registry["registry_revision"] - 1
    with pytest.raises(ValueError, match="STALE_REGISTRY_REVISION"):
        plan_transition(registry, application, transition, event["event_id"])


def test_release_readiness_fails_closed_until_journeys_artifacts_and_defects_clear():
    plan = load_json(ROOT / "state/delivery-plans/docvault-lasttime-fusion-v0.1.json")
    result = evaluate_release_readiness(plan, evaluated_at="2026-09-03T11:00:00Z")
    validate(result, ROOT / "schemas/v1/release-readiness.schema.json")
    assert result["ready"] is False
    assert result["required_journeys_pass"] is False
    assert result["required_artifacts_pass"] is False

    completed = json.loads(json.dumps(plan))
    completed["status"] = "ACTIVE"
    for journey in completed["user_journeys"]:
        journey["status"] = "PASS"
        for criterion in journey["acceptance_criteria"]:
            criterion["status"] = "PASS"
    for deliverable in completed["deliverables"]:
        if deliverable["required_for_train"]:
            deliverable["status"] = "PASS"
            deliverable["evidence"] = ["Verified fixture evidence"]
    completed["defects"] = [
        {"defect_id": "SECURITY_BLOCKER", "severity": "CRITICAL", "status": "OPEN", "summary": "fixture"}
    ]
    assert evaluate_release_readiness(completed, evaluated_at="2026-09-03T11:00:00Z")["ready"] is False
    completed["defects"][0]["status"] = "FIXED"
    assert evaluate_release_readiness(completed, evaluated_at="2026-09-03T11:00:00Z")["ready"] is True

    completed["status"] = "PAUSED"
    assert evaluate_release_readiness(completed, evaluated_at="2026-09-03T11:00:00Z")["ready"] is False
    completed["status"] = "ACTIVE"
    completed["user_journeys"][0]["acceptance_criteria"][0]["status"] = "NOT_STARTED"
    assert evaluate_release_readiness(completed, evaluated_at="2026-09-03T11:00:00Z")["ready"] is False
    completed["user_journeys"][0]["acceptance_criteria"][0]["status"] = "PASS"
    completed["deliverables"][0]["evidence"] = []
    assert evaluate_release_readiness(completed, evaluated_at="2026-09-03T11:00:00Z")["ready"] is False


def test_source_bundle_is_valid_and_apkm_is_an_accepted_intake_format():
    bundle = load_json(ROOT / "intake/source-bundles/docvault-lasttime-fusion.json")
    validate(bundle, ROOT / "schemas/v1/source-bundle.schema.json")
    assert len(bundle["sources"]) == 5

    request = {
        "schema_version": "1.0.0",
        "request_id": "57797468-d68a-4ea3-8157-ef13b5c516eb",
        "submitted_by": "authenticated-user",
        "submitted_at": "2026-09-02T16:01:38Z",
        "source": {
            "kind": "GOOGLE_DRIVE",
            "locator": "drive-folder-and-chunk-manifest",
            "sha256": "2f62abc367c8e34c6234bde6108c5b317aec027e132237a8673cf43c11cb0a52",
            "file_name": "APK.apkm"
        },
        "authorization_profile": {
            "profile_id": "f49bf440-edff-4b89-9305-d2c0ce841aaa",
            "rights_basis": "OTHER_DOCUMENTED_BASIS",
            "static_analysis_allowed": True,
            "dynamic_analysis_allowed": False,
            "network_interception_allowed": False,
            "accepted_by": "authenticated-user",
            "accepted_at": "2026-09-02T16:01:38Z",
            "constraints": ["Fixture only; no authorization is asserted by this test."]
        }
    }
    validate(request, ROOT / "schemas/v1/intake-request.schema.json")


def test_project_selection_is_automatic_for_one_and_interactive_for_many():
    registry = {"applications": []}
    first = {
        "app_id": "alpha-app",
        "display_name": "Alpha",
        "active_for_selection": True,
    }
    second = {
        "app_id": "beta-app",
        "display_name": "Beta",
        "active_for_selection": True,
    }
    registry["applications"] = [first]
    assert select_application(registry)["selected_app_id"] == "alpha-app"
    assert select_application(registry)["selection_decision"] == "AUTO_SELECTED"

    registry["applications"] = [second, first]
    decision = select_application(registry)
    assert decision["selection_decision"] == "USER_SELECTION_REQUIRED"
    assert decision["selected_app_id"] is None
    assert decision["candidate_app_ids"] == ["alpha-app", "beta-app"]


def test_approval_envelope_and_product_attestation_are_separate():
    dossier = {
        "schema_version": "1.0.0",
        "dossier_id": "290d8c48-13c7-4d91-a6c8-5a69e700e745",
        "run_id": "0aa961a9-35ad-4819-8e20-c6ad50d8ea69",
        "source_records": [],
        "decisions": [],
    }
    blueprint = {
        "schema_version": "1.0.0",
        "blueprint_id": "edb18f90-e199-4906-982f-407978a493c4",
        "product_thesis": "fixture",
        "target_platforms": {"android": True, "ios": True},
        "release_scope": "CROSS_PLATFORM_PRODUCT",
        "modules": [],
        "acceptance": {},
    }
    envelope, attestation = create_approval_artifacts(dossier, blueprint, "authenticated-user", "a" * 64)
    assert "foundry_dossier_sha256" in envelope
    assert "foundry_dossier_sha256" not in attestation
    assert envelope["product_blueprint_sha256"] == attestation["product_blueprint_sha256"]


def test_run_registration_is_idempotent(tmp_path):
    request = {
        "schema_version": "1.0.0",
        "request_id": "ecce5b1e-791d-47b3-beac-d4aad4a719fe",
        "submitted_by": "authenticated-user",
        "submitted_at": "2026-09-02T00:00:00Z",
    }
    first = create_run(request, tmp_path)
    second = create_run(request, tmp_path)
    assert first == second
    assert (first / "events.jsonl").read_text(encoding="utf-8").count("RUN_REGISTERED") == 1
