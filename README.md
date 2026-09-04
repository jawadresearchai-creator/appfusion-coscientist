# AppFusion CoScientist — Capability Foundry

**Free-only correction (2026-09-04):** no billing, paid services or top-ups.
Monthly free tiers are not the permanent solution. The user authorized the new
[public Product repository](https://github.com/jawadresearchai-creator/appfusion-product-public)
for standard Linux/macOS CI. All original private workflows remain disabled;
Drive and both original repositories remain private. Local execution is optional.
See `docs/operations/PUBLIC_PRODUCT_EXECUTION.md` and the current event tail.

This private repository is the authoritative Capability Foundry and cloud control plane for AppFusion. It accepts authorized application-analysis requests, records provenance, produces source-aware Foundry dossiers, and emits clean-room Product Blueprints for explicit human approval.

## Execution model

- **Cloud first:** GitHub, GitHub Actions, and Google Drive hold durable state and artifacts.
- **Control-surface neutral:** ChatGPT web, Codex, a persistent API coordinator, and the optional local CLI all submit the same versioned request contracts.
- **Local optional:** no canonical workflow, schema, or artifact contains a required local path.
- **Clean room:** raw/decompiled material remains in the Capability Foundry. The Product Foundry receives only an approved positive-schema `ProductBlueprint` and sanitized approval attestation.
- **Honest autonomy:** the initial target is `FOUNDRY_VERTICAL_SLICE_ALPHA`; `SYSTEM_V1_UA` additionally requires a persistent reasoning coordinator available without new service charges.
- **Session continuity:** every new control surface bootstraps from the conflict-safe Git event ledger; Drive projections and chat memory are never allowed to overwrite a newer committed revision.
- **Essential GitHub only:** reasoning and bulky working artifacts stay in ChatGPT/Drive, while GitHub is reserved for source, reproducible gates, checkpoints, and releases.

## Current bootstrap status

The repositories and Drive workspace exist. Delivery Orchestration v1.1 provides conflict-safe state transitions, a release train, journey gates and bounded repairs. J1 is accepted on Android/iOS; revision 24 restored the authorized single workflow, and revision 25 accepted J2 shared contracts. Revision 26 / milestone 012 delivers an installed-tested Android activity/cadence/history UI preview and public development APK/source ZIP. One clipped UI-test target was repaired; candidate and main Android gates pass. J2 remains IN_PROGRESS: native notifications and iOS activity UI are next, followed by J3 and final security/UX/signing/release gates. Existing J1 evidence/releases remain preserved. The separate Project B worker and Drive state are out of scope and must not be accessed. Read the live registry/event tail before resuming. Untrusted dynamic APK execution remains blocked until a runner proves the required isolation and egress controls.

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
