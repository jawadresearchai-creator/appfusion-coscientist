---
name: appfusion-operator
description: Submit, inspect, resume, or audit AppFusion Capability Foundry and Product Foundry runs through GitHub and Google Drive without requiring a local environment.
---

# AppFusion Operator

Treat GitHub and the configured private Drive hierarchy as canonical. A local filesystem is optional and must not become the only location for state or artifacts.

At the start of each session, read `environment-manifest.json` and the GitHub registry mirror, then reconcile it with the freshest valid `APPFUSION_PROJECT_REGISTRY.json` in Drive `00_CONTROL`. Do not substitute chat memory for this bootstrap. Use the highest valid registry revision; pause on an unresolved equal-revision conflict.

Apply the registry selection rule before product work: report zero active apps, automatically resume exactly one active app, or list multiple active apps and ask the user which one to continue. Always report the selected checkpoint, last completed event, blockers, and next safe action.

Before starting an APK run:

1. Confirm the input is in the private intake location and obtain its immutable file identity and SHA-256.
2. Require an explicit `AnalysisAuthorizationProfile`; do not infer ownership or permission.
3. Create a schema-valid `IntakeRequest` in the Capability Foundry and monitor the resulting run events.
4. Respect stage outcomes. A blocked or skipped stage is not a pass.

Keep source-aware material in the Capability Foundry. Transfer only a positive-schema `ProductBlueprint` and sanitized `ProductApprovalAttestation` to the Product Foundry.

Never begin synthesized Product implementation until the user explicitly approves the exact Product Blueprint hash. After approval, continue without routine prompts; pause only for user intervention, a material blueprint deviation, or a mandatory authorization, security, environment, or budget gate.

Report the demonstrated autonomy label accurately. Interactive ChatGPT/Codex operation is not `SYSTEM_V1_UA`; that label requires the deployed persistent coordinator.

Route reasoning, comparison, reports, frequent state updates, and bulky artifacts through ChatGPT and Drive. Use GitHub only for version-controlled source/contracts, small milestone or approval mirrors, reproducible build/test/security gates, and releases. After a material transition, update Drive state immediately; mirror it to GitHub only at code, approval, milestone, or release boundaries.
