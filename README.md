# AppFusion CoScientist — Capability Foundry

This private repository is the authoritative Capability Foundry and cloud control plane for AppFusion. It accepts authorized application-analysis requests, records provenance, produces source-aware Foundry dossiers, and emits clean-room Product Blueprints for explicit human approval.

## Execution model

- **Cloud first:** GitHub, GitHub Actions, and Google Drive hold durable state and artifacts.
- **Control-surface neutral:** ChatGPT web, Codex, a persistent API coordinator, and the optional local CLI all submit the same versioned request contracts.
- **Local optional:** no canonical workflow, schema, or artifact contains a required local path.
- **Clean room:** raw/decompiled material remains in the Capability Foundry. The Product Foundry receives only an approved positive-schema `ProductBlueprint` and sanitized approval attestation.
- **Honest autonomy:** the initial target is `FOUNDRY_VERTICAL_SLICE_ALPHA`; `SYSTEM_V1_UA` additionally requires a persistent metered reasoning coordinator.

## Current bootstrap status

The repositories and Drive workspace exist. Contract validation, deterministic run creation, static APK inventory, clean-room schemas, policy checks, and CI are bootstrapped. Untrusted dynamic execution remains blocked until a runner proves the required isolation and egress controls.

Run locally only if desired:

```bash
python -m pip install -e .[dev]
appfusion bootstrap-check
pytest
```

Canonical documents:

- `docs/architecture/APPFUSION_COSCIENTIST_SYSTEM_BLUEPRINT_v1.0_LOCKED.md`
- `docs/audit/V0.12_LOCK_AUDIT.md`
- `docs/operations/CHATGPT_WEB_OPERATOR.md`

The archived v0.11 draft and v0.12 errata are retained as non-normative review evidence.
Private AppFusion Capability Foundry and cloud-first orchestration control plane
