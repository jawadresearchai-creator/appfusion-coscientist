---
name: appfusion-operator
description: Submit, inspect, resume, or audit AppFusion Capability Foundry and Product Foundry runs through GitHub and Google Drive without requiring a local environment.
---

# AppFusion Operator

Treat GitHub and the configured private Drive hierarchy as canonical. A local filesystem is optional and must not become the only location for state or artifacts.

Before starting an APK run:

1. Confirm the input is in the private intake location and obtain its immutable file identity and SHA-256.
2. Require an explicit `AnalysisAuthorizationProfile`; do not infer ownership or permission.
3. Create a schema-valid `IntakeRequest` in the Capability Foundry and monitor the resulting run events.
4. Respect stage outcomes. A blocked or skipped stage is not a pass.

Keep source-aware material in the Capability Foundry. Transfer only a positive-schema `ProductBlueprint` and sanitized `ProductApprovalAttestation` to the Product Foundry.

Never begin synthesized Product implementation until the user explicitly approves the exact Product Blueprint hash. After approval, continue without routine prompts; pause only for user intervention, a material blueprint deviation, or a mandatory authorization, security, environment, or budget gate.

Report the demonstrated autonomy label accurately. Interactive ChatGPT/Codex operation is not `SYSTEM_V1_UA`; that label requires the deployed persistent coordinator.
