from __future__ import annotations

import argparse
import json
from pathlib import Path

from .approval import write_approval_artifacts
from .bootstrap import bootstrap_check
from .contracts import load_json, validate
from .state import create_run
from .static_inventory import write_inventory
from .orchestration import evaluate_release_readiness, validate_control_state


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(prog="appfusion")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("bootstrap-check")
    sub.add_parser("orchestration-check")

    readiness = sub.add_parser("release-readiness")
    readiness.add_argument("delivery_plan", type=Path)
    readiness.add_argument("--evaluated-at", required=True)

    create = sub.add_parser("create-run")
    create.add_argument("request", type=Path)
    create.add_argument("--output-root", type=Path, default=Path("runs"))

    inventory = sub.add_parser("static-inventory")
    inventory.add_argument("apk", type=Path)
    inventory.add_argument("output", type=Path)

    approve = sub.add_parser("approve-blueprint")
    approve.add_argument("dossier", type=Path)
    approve.add_argument("blueprint", type=Path)
    approve.add_argument("--approver-principal", required=True)
    approve.add_argument("--output-root", type=Path, required=True)

    args = parser.parse_args()
    root = repository_root()
    if args.command == "bootstrap-check":
        errors = bootstrap_check(root)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("AppFusion bootstrap contracts: PASS")
        return 0
    if args.command == "orchestration-check":
        errors = validate_control_state(root)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("AppFusion delivery orchestration state: PASS")
        return 0
    if args.command == "release-readiness":
        plan = load_json(args.delivery_plan)
        validate(plan, root / "schemas/v1/delivery-plan.schema.json")
        readiness = evaluate_release_readiness(plan, evaluated_at=args.evaluated_at)
        validate(readiness, root / "schemas/v1/release-readiness.schema.json")
        print(json.dumps(readiness, sort_keys=True))
        return 0 if readiness["ready"] else 3
    if args.command == "create-run":
        request = load_json(args.request)
        validate(request, root / "schemas" / "v1" / "intake-request.schema.json")
        print(create_run(request, args.output_root))
        return 0
    if args.command == "static-inventory":
        write_inventory(args.apk, args.output)
        print(args.output)
        return 0
    if args.command == "approve-blueprint":
        validate(load_json(args.dossier), root / "schemas/v1/foundry-decision-dossier.schema.json")
        validate(load_json(args.blueprint), root / "schemas/v1/product-blueprint.schema.json")
        envelope, attestation = write_approval_artifacts(
            args.dossier,
            args.blueprint,
            args.approver_principal,
            root / "policies",
            args.output_root,
        )
        validate(load_json(envelope), root / "schemas/v1/approval-envelope.schema.json")
        validate(load_json(attestation), root / "schemas/v1/product-approval-attestation.schema.json")
        print(envelope)
        print(attestation)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
