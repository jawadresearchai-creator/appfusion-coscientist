# AppFusion CoScientist
## Canonical System Blueprint — v1.0 LOCKED

**Locked:** 2026-09-02  
**Implementation target:** `FOUNDRY_VERTICAL_SLICE_ALPHA`  
**Normative authority:** this document supersedes the archived v0.11 draft and v0.12 errata.

## 1. Mission

AppFusion autonomously analyzes one or more user-authorized Android application packages, discovers their capabilities, compares overlapping implementations, retains valuable unique capabilities, and specifies a coherent modular product. After explicit approval of a clean-room Product Blueprint, the Product Foundry independently implements, builds, tests, repairs, audits, and releases the approved Android/iOS product.

The system compares capabilities below the app level. A capability may be unique, overlapping, partially overlapping, complementary, conflicting, unavailable, server-dependent, or not sufficiently observable. “Best” is asserted only from evidence appropriate to the claim.

## 2. Non-negotiable rules

1. Only user-owned, licensed, or explicitly authorized inputs are analyzed.
2. Raw/decompiled source-aware evidence remains in the private Capability Foundry.
3. Product implementation receives no raw Foundry context or source-identifying behavioral reference.
4. Every generated `ProductBlueprint` requires explicit, authenticated, hash-bound human approval.
5. Product work proceeds autonomously after approval unless a material deviation, authorization, security, budget, or user-intervention gate blocks it.
6. The first-module checkpoint is published and execution continues; it is not another approval gate.
7. Android and iOS are mandatory whenever the approved blueprint targets both. An Android-only result is an explicitly labeled experimental pilot.
8. Paid overage is disabled by default.
9. Local infrastructure is optional. Cloud state and cloud execution are authoritative.
10. Decompiled third-party implementation is evidence, not Product source. Product code is independently implemented unless a separately authorized reuse route applies.

## 3. Cloud-first, control-surface-neutral architecture

Canonical durable state lives in:

- the private Capability Foundry GitHub repository;
- the separate Product Foundry GitHub repository;
- private Google Drive/object storage for binaries, reports, and releases;
- append-only run and approval event records;
- immutable workflow artifacts and release attestations.

Supported control surfaces are:

- ChatGPT web with authenticated GitHub and Google Drive plugins;
- Codex desktop;
- a persistent coordinator using an authorized reasoning-runtime API;
- an optional local CLI/operator.

Every surface submits the same versioned `IntakeRequest`, approval, deviation, and control contracts. A surface may disappear without erasing canonical state. No workflow requires a workstation path, local emulator, active Codex session, or local credential.

ChatGPT web and Codex may deliver `INTERACTIVE_RESUMABLE` reasoning. They do not alone demonstrate unattended reasoning after the chat closes. `SYSTEM_V1_UA` requires the persistent coordinator.

## 4. Planes and adapters

### Control plane

Performs reasoning, evidence synthesis, capability classification, comparison, architecture decisions, Product Blueprint generation, approval handling, deviation analysis, and repair diagnosis.

### Execution plane

Performs deterministic intake, hashing, tool restoration, static analysis, authorized dynamic analysis, benchmarks, builds, tests, artifact promotion, and signing. GitHub Actions is the default implementation; compatible cloud runners may replace it.

### Access plane

Uses narrowly scoped GitHub and Google Drive/object-store identities. A ChatGPT connector credential is not assumed to exist inside CI. The CI Drive adapter uses workload identity or another explicitly approved cloud credential.

### Optional local adapter

May validate contracts, inspect authorized artifacts, or reproduce failures. It is never canonical and cannot be the only route to build, test, resume, or release.

## 5. Repository and storage topology

### Capability Foundry — private

Contains orchestration code, policies, schemas, tool registry, source-aware records, evidence indexes, Foundry decisions, benchmark definitions, and clean-room export code. Raw APKs and bulk decompilation outputs remain outside Git history in private bounded storage.

### Product Foundry — private by default

Contains only independently written product code, approved clean-room Product Blueprints, sanitized approval attestations, Product tests, build configuration, and release records. Its automation has no Foundry read credential.

### Drive/object storage

- private intake;
- private Foundry reports;
- clean-room blueprints;
- Product releases;
- audits;
- quarantine.

Product principals receive access only to Product-facing storage paths and artifacts required by policy.

## 6. Clean-room and approval objects

### `FoundryDecisionDossier`

Private and source-aware. It may contain source identities, hashes, signatures, decompilation references, raw benchmark evidence, rights records, source-specific winner/rejection reasoning, and Foundry-only security findings.

### `ProductBlueprint`

Product-facing and positive-schema-only. It contains product thesis, source-independent behavioral targets, modules, shared-core contracts, engine feasibility records, platform strategy, measurable acceptance, security/privacy constraints, implementation order, and unresolved Product-relevant uncertainty without source identity leakage.

### `ApprovalEnvelope`

Immutable approval of one exact Product Blueprint hash, with approver principal, time, Foundry dossier hash, policy hash, and schema version. It is created only by explicit human approval.

### `ProductApprovalAttestation`

A derived sanitized transfer object containing only the approval identity, Product Blueprint hash, approval status/time, policy/schema versions, and conditions.

### Approval lifecycle

An `ApprovalEnvelope` is never mutated. Revocation and supersession are append-only `ApprovalEvent` records. Any semantic Product Blueprint change invalidates prior approval and requires a new envelope.

## 7. Foundry pipeline

1. Register an `IntakeRequest` with immutable locator and expected SHA-256.
2. Enforce `AnalysisAuthorizationProfile` before retrieval or analysis.
3. Retrieve into a hostile-input lane; verify size, type, hash, signature/provenance, and package structure.
4. Restore the reviewed, pinned toolchain.
5. Perform static analysis: manifest, resources, DEX, SDK/engine fingerprints, native inventory, permissions, components, storage, networking indicators, and coverage limitations.
6. Perform authorized dynamic analysis only in a lane meeting the required security profile.
7. Extract normalized capabilities and evidence, including blocked/absent/inconclusive distinctions.
8. Classify relationships: unique, exact overlap, partial overlap, complementary, or conflict.
9. Benchmark only claims with objective, versioned fixtures and declared metrics.
10. Select behavioral targets and evaluate Product engine candidates separately.
11. Produce the private `FoundryDecisionDossier`.
12. Compile a positive-schema `ProductBlueprint`; run leakage canaries and independent transfer validation.
13. Present dossier and blueprint for explicit approval.
14. Transfer only approved Product-facing objects.

## 8. Product Engine Feasibility Gate

The lifecycle is:

`ObservedReferenceImplementation -> BehavioralTarget -> ProductEngineCandidate -> ProductModuleImplementation`

Critical engines cannot become locked Product dependencies until license compatibility, Android/iOS compatibility for the target scope, minimal build/integration probes, representative functional probes, material size/runtime/dependency constraints, security/maintenance risk, and any relevant objective benchmark are recorded.

Pre-Blueprint feasibility probes are nonproduction experiments and do not implement the Product.

## 9. Product architecture

The default is Kotlin Multiplatform with modular shared business logic and native/platform adapters where quality or platform APIs require them. This is a preference, not an untested engine decision.

Every module declares:

- capability IDs and behavioral targets;
- inputs, outputs, routes, and UI entry points;
- service/API/event/data contracts;
- platform support and adapters;
- permissions, privacy, security, offline, and migration behavior;
- dependencies and replaceability boundaries;
- unit, integration, platform, acceptance, and regression tests.

Shared services include identity, secure storage, files, search, notifications, scheduling, permissions, database, backup/sync, settings, navigation, telemetry policy, and an activity event bus. Unique features become modules; unrelated features are composed through contracts and coherent UX rather than placed in a feature pile.

## 10. Platform acceptance

For `target_platforms.android=true` and `target_platforms.ios=true`, Product acceptance requires Android build/tests, iOS simulator build/tests, shared tests, platform-adapter contract tests, and no known platform-blocking critical defect.

Unavailable iOS infrastructure records `PAUSED_CI_BUDGET`, `BLOCKED_BUDGET`, or `BLOCKED_ENVIRONMENT` as applicable; it cannot pass Product v1. Simulator, physical-device, signed IPA, TestFlight, and App Store readiness are separate states.

## 11. Security lanes

Any parser or process influenced by an APK is untrusted. Its lane uses no production, Product, signing, or deployment secrets; no Product checkout; no shared privileged cache; pinned actions/images; disabled checkout credential persistence; no privileged `pull_request_target`; denied cloud metadata; denied or mediated egress; and schema/size/path/symlink validation before one-way promotion.

`permissions: {}` disables usable `GITHUB_TOKEN` repository permissions but is not a complete sandbox. If egress or metadata isolation cannot be demonstrated, the stage outcome is `BLOCKED_SECURITY_ENVIRONMENT`.

Release signing is a separate protected `ReleaseSigner` principal/environment after verified promotion.

## 12. State, outcomes, and evidence

Run state and stage outcome are separate.

Canonical outcomes are:

`PASS`, `FAIL`, `SKIPPED_NOT_APPLICABLE`, `SKIPPED_POLICY`, `BLOCKED_AUTHORIZATION`, `BLOCKED_ENVIRONMENT`, `BLOCKED_SECURITY_ENVIRONMENT`, `BLOCKED_BUDGET`, `INCONCLUSIVE`, `CANCELLED`.

Paused states include:

`PAUSED_MODEL_CAPACITY`, `PAUSED_REASONING_RUNTIME`, `PAUSED_CI_BUDGET`, `PAUSED_AUTHORIZATION`, `PAUSED_BLUEPRINT_REVOKED`, `PAUSED_USER_INTERVENTION`.

Events are append-only, ordered, idempotent, and reconciled by a single writer. Evidence records dependencies on input, tool, model/runtime, prompt/template, fingerprint database, fixture, policy, authorization, license decision, and environment versions. Dependency changes propagate suspect/retest/reconciliation/blueprint-integrity/release-risk states without automatic destructive withdrawal.

## 13. Milestones and truthful labels

### `FOUNDRY_VERTICAL_SLICE_ALPHA`

Proves authorized APK intake, fixed core tools, static analysis, permitted ordinary runtime analysis, normalized extraction, one overlap decision, one unique decision, benchmarkability triage, behavioral-target conversion, clean-room export, Product Blueprint generation, approval workflow, append-only resume, and leakage canaries. It does not prove generalized inference quality.

### `FOUNDRY_V1_TRUSTED`

Adds frozen calibration and holdout corpora, pre-registered evaluation, hierarchical capability scoring, contamination controls, repeated semantic-stability evaluation, confidence calibration, and closure of high-impact failures.

### `PRODUCT_V1`

Requires an approved Product Blueprint originating from a trusted Foundry run for the relevant domains. Alpha output may produce only `EXPERIMENTAL_PILOT_PRODUCT`.

### `SYSTEM_V1_IR`

Requires trusted Foundry and Product v1 plus interruption-safe interactive-resumable model/control operation.

### `SYSTEM_V1_UA`

Adds persistent coordinator, durable queue, runtime adapter, provider policy, explicit model budget, leases/heartbeats/resume, and demonstrated unattended build/test/repair. Only this may be called `FULL_SYSTEM_V1`.

## 14. Evaluation and budget

Foundry trust uses a pre-registered protocol with frozen taxonomy/domain scope, calibration and holdout hashes, label distribution, minimum sample size selected before evaluation, at least three repeats, model/prompt versions, scoring rules, confidence intervals, partially observable policy, independent adjudication, and contamination controls.

Budgets are tracked separately for CI compute, metered model runtime, storage, third-party services, and signing/distribution. `paid_overage_authorized=false` is the default. Exhaustion preserves state and blocks/pauses rather than silently spending or reducing analytical quality.

## 15. Release and evolution

After the first approved Product module passes acceptance, publish `FirstModuleCheckpoint` and continue automatically unless the user intervenes or a mandatory gate blocks.

Release records bind the Product Blueprint hash, approval ID, source commit, dependency lockfiles, SBOM, tests, security/license results, environment snapshots, provenance/attestations, and artifact hashes. Android APK/AAB, iOS build states/artifacts as authorized, source archives, reports, screenshots, and checksums are delivered to GitHub Releases and approved Drive folders.

New apps enter the same Foundry. Unique valuable capabilities are proposed as modules; overlaps are compared against current registry incumbents; replacements trigger dependent regression tests. Rejected candidates and reasons remain durable knowledge.

## 16. Initial implementation order

1. Provision the two private repositories and private Drive topology.
2. Lock schemas, policies, cloud-authoritative manifest, and control-surface contract.
3. Validate CI, state/outcome vocabulary, approval immutability, and clean-room canaries.
4. Configure cloud Drive retrieval identity.
5. Build and attest the pinned static-analysis image and Tool Registry.
6. Prove the untrusted static lane before APK #1.
7. Run the first authorized APK through the Alpha path.
8. Generate, review, and explicitly approve or reject its Product Blueprint.

No synthesized Product implementation starts before step 8 approval.
