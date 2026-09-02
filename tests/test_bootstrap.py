import json
import zipfile
from pathlib import Path

from appfusion_foundry.bootstrap import bootstrap_check
from appfusion_foundry.approval import create_approval_artifacts
from appfusion_foundry.contracts import STAGE_OUTCOMES, load_json, validate
from appfusion_foundry.state import create_run
from appfusion_foundry.static_inventory import inventory_apk
from appfusion_foundry.project_registry import select_application


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


def test_project_registry_is_valid_and_has_no_active_product_yet():
    registry = load_json(ROOT / "state/APPFUSION_PROJECT_REGISTRY.json")
    validate(registry, ROOT / "schemas/v1/project-registry.schema.json")
    assert select_application(registry) == {
        "selection_decision": "NO_ACTIVE_APPLICATIONS",
        "selected_app_id": None,
        "candidate_app_ids": [],
    }


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
