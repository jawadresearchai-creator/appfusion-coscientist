# AppFusion CoScientist — Capability Foundry

This private repository is the authoritative Capability Foundry and cloud control plane for AppFusion. It accepts authorized application-analysis requests, records provenance, produces source-aware Foundry dossiers, and emits clean-room Product Blueprints for explicit human approval.

## Execution model

- **Cloud first:** GitHub, GitHub Actions, and Google Drive hold durable state and artifacts.
- **Control-surface neutral:** ChatGPT web, Codex, a persistent API coordinator, and the optional local CLI all submit the same versioned request contracts.
- **Local optional:** no canonical workflow, schema, or artifact contains a required local path.
- **Clean room:** raw/decompiled material remains in the Capability Foundry. The Product Foundry receives only an approved positive-schema `ProductBlueprint` and sanitized approval attestation.
- **Honest autonomy:** the initial target is `FOUNDRY_VERTICAL_SLICE_ALPHA`; `SYSTEM_V1_UA` additionally requires a persistent metered reasoning coordinator.
- **Session continuity:** every new control surface bootstraps from the conflict-safe Git event ledger; Drive projections and chat memory are never allowed to overwrite a newer committed revision.
- **Essential GitHub only:** reasoning and bulky working artifacts stay in ChatGPT/Drive, while GitHub is reserved for source, reproducible gates, checkpoints, and releases.

## Current bootstrap status

The repositories and Drive workspace exist. Delivery Orchestration v1.1 adds conflict-safe state transitions, an explicit release train, end-to-end journey gates, bounded repair/audit loops, and fail-closed release readiness. Milestone 009 produced genuine Android and iOS application artifacts. Milestone 010 passed installed Android J1 on the optional local executor and stored the tested APK, source ZIP, screenshot, evidence and checksums in Drive. The train is paused before iOS J1 because hosted Actions report an account billing/spending-limit block and the available local host cannot run an iOS Simulator. J2/J3, signing and final cross-platform release gates remain incomplete. Untrusted dynamic APK execution remains blocked until a runner proves the required isolation and egress controls.

Run locally only if desired:

```bash
python -m pip install -e .[dev]
appfusion bootstrap-check
pytest
```

Canonical documents:

- `docs/architecture/APPFUSION_COSCIENTIST_SYSTEM_BLUEPRINT_v1.0_LOCKED.md`
- `docs/architecture/APPFUSION_DELIVERY_ORCHESTRATION_BLUEPRINT_v1.1.md`
- `docs/audit/APPFUSION_DELIVERY_ORCHESTRATION_v1.1_AUDIT.md`
- `docs/audit/V0.12_LOCK_AUDIT.md`
- `docs/operations/CHATGPT_WEB_OPERATOR.md`
- `docs/operations/NEW_CHAT_BOOTSTRAP.md`

The archived v0.11 draft and v0.12 errata are retained as non-normative review evidence.
Private AppFusion Capability Foundry and cloud-first orchestration control plane
