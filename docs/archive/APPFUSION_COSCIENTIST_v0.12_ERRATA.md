# AppFusion CoScientist — v0.12 Lock-Candidate Errata

**Status:** Lock-candidate normative amendment to `APPFUSION_COSCIENTIST_SYSTEM_BLUEPRINT_v0.11_SECURITY_AUTONOMY_CLEANROOM_CLOSURE_DRAFT.md`  
**Date:** 2026-09-02  
**Purpose:** Close the remaining specification ambiguities identified in the final v0.11 adversarial review without redesigning the architecture. Where this errata conflicts with v0.11, **this errata controls**. The final v1.0 LOCKED document shall consolidate v0.11 + this errata into one canonical blueprint.

---

## 0. Lock-candidate decision

The v0.11 architecture is retained. No reviewer is treated as authoritative. The following final-review points are accepted because they expose real specification ambiguity or operational risk:

1. Separate the source-aware Foundry dossier from the clean-room Product Blueprint and from the approval record.
2. Separate the first vertical-slice alpha milestone from a trusted/generalized Foundry v1 claim.
3. Make iOS build/test mandatory whenever the approved Product Blueprint targets iOS.
4. Convert hostile/untrusted-runner controls from descriptive prose into machine-verifiable workflow policy.
5. Separate `SYSTEM_V1_IR` from `SYSTEM_V1_UA`; do not call interactive-resumable operation the full unattended goal.
6. Add a Product Engine Feasibility Gate before critical engines may be locked into a Product Blueprint.
7. Align schemas, state outcomes and evidence invalidation with entities already introduced by v0.11.
8. Strengthen Foundry self-evaluation protocol, data/budget semantics and release signing.

The following prior design decisions remain unchanged:

- **Every Product Blueprint requires explicit human approval before Product implementation begins.** There is no mature-system auto-approval bypass for the initial Product Blueprint.
- The **First-Module Checkpoint Report is non-blocking**: it is published after the first approved module passes acceptance and the pipeline continues automatically unless the user intervenes or a material deviation is detected.
- The **Tool Acquisition Engine remains part of the ultimate architecture**, but its fully autonomous implementation is not a prerequisite for the first Foundry vertical slice.
- Model reasoning remains **model-led, evidence-driven and tool-augmented**. Tools are not preferred merely to save tokens.
- The ultimate architecture retains both `INTERACTIVE_RESUMABLE` and true `UNATTENDED_AGENTIC` execution modes.
- GitHub-hosted ephemeral VMs remain acceptable for the defined low-risk execution lanes; they are not represented as a universal hardened malware laboratory.

---

# 1. Three-artifact Blueprint / clean-room approval model

## 1.1 Problem closed

v0.11 used the phrase “Product Blueprint” for both human review material containing Foundry-side details and the clean-room artifact that the Product implementation context may receive. Those are not the same information object.

The system SHALL use three separate artifacts.

## 1.2 `FoundryDecisionDossier`

**Classification:** private, source-aware, Capability Foundry only.

May contain:

- input application identities and versions;
- hashes/signing certificates/source provenance;
- JADX/apktool/Androguard/Ghidra/native references;
- source-aware evidence and internal opaque-ID reverse mappings;
- benchmark raw data tied to source applications;
- source-specific rejection/winner reasoning;
- rights/analysis authorization records;
- Foundry-only security findings;
- complete audit provenance.

The Product implementation principal SHALL NOT have read access to this artifact.

## 1.3 `ProductBlueprint`

**Classification:** clean-room, Product-facing, positive-schema export.

This is the artifact that constrains Product implementation. It may contain only fields allowed by the versioned clean-room export schema, including:

- product thesis;
- selected modules and shared-core contracts;
- source-independent capability specifications;
- `BehavioralTarget` records;
- opaque capability/spec IDs with no source reverse mapping;
- test fixtures that are independently permitted to cross;
- measurable acceptance thresholds;
- Product Engine candidates and feasibility states;
- module/API/event/data contracts;
- Android/iOS/KMP/native implementation strategy;
- security/privacy/permissions/offline requirements;
- license-compatible Product engine decisions;
- implementation order;
- QA/release acceptance requirements;
- unresolved Product-relevant uncertainty expressed without source identity leakage.

The `ProductBlueprint` SHALL NOT contain:

- source app names/package names as behavioral references;
- source-aware input inventories;
- decompiled text/assets/resources;
- raw proprietary identifiers not independently public/necessary;
- Foundry-only evidence locations;
- instructions to reproduce a named source implementation.

## 1.4 `ApprovalEnvelope`

The human approval event SHALL create an immutable `ApprovalEnvelope` containing at minimum:

```yaml
approval_id: <uuid>
foundry_dossier_sha256: <hash>
product_blueprint_sha256: <hash>
approver_principal: <authenticated-user-id-or-approved-principal>
approved_at: <timestamp>
policy_bundle_hash: <hash>
clean_room_schema_version: <version>
approval_status: APPROVED | REJECTED | SUPERSEDED | REVOKED
conditions: []
```

The user may inspect both the `FoundryDecisionDossier` and the `ProductBlueprint` before approval.

The Product Foundry receives only:

- the approved `ProductBlueprint`;
- a **sanitized Product approval attestation** containing `approval_id`, `product_blueprint_sha256`, approval status, timestamp, policy/schema versions and applicable conditions.

The full `ApprovalEnvelope` remains in the audit/control plane. The Product agent does not need the Foundry dossier or its contents.

## 1.5 Approval semantics

Approval binds a specific Product Blueprint hash. Any change to the Product Blueprint after approval invalidates that approval unless the change is explicitly classified as non-semantic metadata under policy. Material changes require a new Approval Envelope through the Blueprint Deviation Gate.

Partial approval remains prohibited for the initial Product Blueprint.

---

# 2. Foundry milestone semantics: Alpha vs Trusted v1

## 2.1 Replace ambiguous “Capability Foundry v1 complete” language

The narrow end-to-end first slice and a trusted/generalized Foundry are now separate milestones.

### `FOUNDRY_VERTICAL_SLICE_ALPHA`

Purpose: prove the complete plumbing against real approved APK input.

Requirements include:

- standard APK intake;
- hash/signature/provenance/authorization gate;
- fixed core toolchain restoration;
- manifest/resource/DEX static analysis;
- initial SDK/engine fingerprinting;
- ordinary non-instrumented emulator execution when allowed;
- normalized capability extraction;
- at least one overlap decision;
- at least one useful unique-capability decision;
- benchmarkability triage and one objective benchmark when the pilot provides a benchmarkable target, otherwise the explicit non-benchmarkable route;
- `ObservedReferenceImplementation -> BehavioralTarget` conversion;
- positive-schema clean-room export;
- Product Blueprint generation;
- mandatory human approval workflow;
- append-only run ledger/resume behavior;
- clean-room canary leakage test.

Passing this milestone proves the Foundry works end to end. It does **not** prove that its inference quality generalizes.

### `FOUNDRY_V1_TRUSTED`

Purpose: certify the supported taxonomy/domains at a declared trust level.

Requires, in addition to the Alpha milestone:

- frozen calibration corpus;
- independently locked holdout corpus;
- pre-registered evaluation protocol;
- required quality thresholds passed on the holdout;
- clean-room leakage tests passed;
- prompt-injection tests passed;
- blocked-vs-absent classification tests passed;
- repeatability/confidence calibration evaluated;
- high-impact failures adjudicated and closed.

The golden/holdout evaluation therefore occurs **before `FOUNDRY_V1_TRUSTED` certification**, even if advanced Foundry expansion continues afterward.

## 2.2 Product use of Alpha output

An Alpha Foundry output may be used to exercise the Product Foundry only under:

```text
EXPERIMENTAL_PILOT_PRODUCT
```

Such a Product may be built/tested to validate the engineering pipeline, but it SHALL NOT be labeled a trusted Product v1 derived from a trusted Foundry.

A normal `PRODUCT_V1` claim requires the input Product Blueprint to originate from a `FOUNDRY_V1_TRUSTED` run for the relevant supported capability domains/taxonomy.

---

# 3. Mandatory iOS acceptance semantics

Android and iOS remain first-class target platforms when the approved Product Blueprint declares both.

## 3.1 Cross-platform Blueprint

If:

```yaml
target_platforms:
  android: true
  ios: true
```

then Product v1 acceptance SHALL require:

- Android build + applicable tests;
- iOS simulator build + applicable tests;
- shared KMP/common tests where relevant;
- platform-specific contract/adaptor tests;
- no known platform-blocking critical defect.

Missing macOS minutes, Xcode availability or iOS infrastructure causes:

```text
PAUSED_CI_BUDGET
```

or

```text
FAILED_BLOCKED_ENVIRONMENT
```

It does **not** count as Product v1 success.

## 3.2 Android-only pilot

An Android-only engineering pilot remains permitted only when the approved Product Blueprint explicitly declares:

```yaml
release_scope: EXPERIMENTAL_ANDROID_ONLY_PILOT
```

It must not be represented as the target Android+iOS Product.

## 3.3 Physical iOS device / distribution state

Simulator success is not equivalent to:

- physical-device validation;
- signed distributable IPA;
- TestFlight readiness;
- App Store readiness.

Those release states remain separately declared.

---

# 4. Enforceable untrusted/hostile runner policy

The S0-S3 security lanes remain, but controls SHALL be machine-verifiable wherever the underlying environment permits it.

## 4.1 Untrusted execution workflow profile

Any job that parses or executes untrusted APK-controlled content SHALL satisfy a versioned `UntrustedRunnerProfile`.

Minimum policy:

```yaml
repository_permissions:
  github_token_permissions: none
  persist_checkout_credentials: false

secrets:
  production_secrets: forbidden
  release_signing_secrets: forbidden
  product_service_credentials: forbidden

checkout:
  private_product_repository: forbidden_in_execution_lane
  untrusted_code_executed_with_privileged_context: forbidden

caches:
  shared_with_privileged_jobs: false

actions:
  pin_to_full_commit_sha: required

triggers:
  privileged_pull_request_target_for_untrusted_execution: forbidden

network:
  default_policy: deny_or_mediated
  authorized_allowlist_required: true

cloud_metadata:
  access: denied

outputs:
  schema_validated: required
  signed_job_manifest: required
  one_way_promotion: required
```

### GitHub token clarification

GitHub creates a per-job `GITHUB_TOKEN`; AppFusion SHALL NOT pretend the token object is absent. Instead, untrusted jobs SHALL configure the token with no usable repository permissions (`permissions: {}` or the strongest equivalent supported by the platform), avoid passing it to untrusted subprocesses, and avoid persisting checkout credentials. Where no checkout is required, no repository checkout occurs at all.

## 4.2 Privilege separation

Untrusted APK execution SHALL NOT share an execution job with:

- canonical registry writes;
- Product source mutation;
- release signing;
- secret-bearing deployment;
- privileged artifact promotion.

A later privileged job may consume untrusted-job output only after validating:

- provenance/job identity;
- declared schema;
- size/count limits;
- expected artifact types;
- signatures/hashes where configured;
- absence of path traversal/symlink tricks;
- applicable malware/content policy.

## 4.3 `workflow_run` / artifact promotion

Privileged workflows triggered after an untrusted workflow SHALL treat upstream artifacts as untrusted data and SHALL NOT execute code or configuration from them merely because the prior workflow succeeded.

## 4.4 Egress enforcement

“Default deny” is an acceptance-tested behavior, not prose. The selected runner implementation must demonstrate that unauthorized egress from the APK/emulator/process is blocked or forced through a mediated proxy. If the environment cannot enforce the required lane policy, the stage becomes:

```text
BLOCKED_SECURITY_ENVIRONMENT
```

rather than silently downgrading isolation.

## 4.5 Release signing isolation

APK/IPA release signing occurs in a separate protected `ReleaseSigner` environment after artifact promotion. No analysis or untrusted-execution job has access to signing material.

---

# 5. System release labels and autonomy truthfulness

The operating-mode distinction introduced in v0.11 now has corresponding product/system release labels.

## 5.1 `SYSTEM_V1_IR`

Demonstrated when:

- `FOUNDRY_V1_TRUSTED` passes;
- `PRODUCT_V1` passes on an approved target;
- the model/control plane can run the analysis/build/repair loop while an authenticated reasoning session is active;
- interruption/resume preserves completed state without unnecessary recomputation;
- no repeated user “proceed” prompts are required for already authorized implementation work.

This is a valid, useful system release, but it is explicitly **interactive-resumable**.

## 5.2 `SYSTEM_V1_UA`

Requires everything in `SYSTEM_V1_IR` plus:

- persistent coordinator;
- durable event queue;
- working reasoning-runtime adapter;
- model/provider availability policy;
- separate metered-model budget authorization when applicable;
- leases/heartbeats/wake-resume behavior;
- unattended build/test/repair continuation demonstrated end to end;
- approval/deviation gates still enforced.

This mode fulfills the original “drop approved inputs and allow the system to continue without an active human/model chat session” target.

## 5.3 “Full System v1” terminology

The unqualified phrase **`FULL_SYSTEM_V1` is reserved for `SYSTEM_V1_UA`**.

Until then, the system SHALL identify itself as `SYSTEM_V1_IR` and SHALL NOT imply unattended model autonomy.

The architectural document may still be versioned `System Blueprint v1.0`; blueprint version and demonstrated runtime release status are different namespaces.

---

# 6. Product Engine Feasibility Gate

A source-app behavioral winner does not establish the Product technology choice.

Critical Product engines SHALL pass a feasibility lifecycle before they can become locked foundations in an approvable Product Blueprint.

## 6.1 Entities remain separate

```text
ObservedReferenceImplementation
        -> BehavioralTarget
        -> ProductEngineCandidate(s)
        -> ProductModuleImplementation
```

## 6.2 Candidate maturity states

```text
DISCOVERED
LICENSE_REVIEWED
PLATFORM_COMPATIBLE
BUILD_PROBED
FUNCTIONALLY_PROBED
BENCHMARKED               # when a relevant objective benchmark exists
APPROVED_CANDIDATE
REJECTED_CANDIDATE
BLOCKED_CANDIDATE
```

## 6.3 Minimum lock conditions

A **critical** engine (office rendering/editing, PDF engine, OCR, encryption/storage engine, media engine, database/storage core or similarly load-bearing technology) SHALL NOT appear as a locked Product Blueprint dependency unless:

- license/use compatibility is reviewed;
- declared Android/iOS compatibility is verified for the approved platform scope;
- a minimal build/integration probe succeeds on required platforms where practical;
- a representative functional probe succeeds;
- material package-size/runtime/dependency constraints are recorded;
- security/maintenance risk is recorded;
- objective benchmark evidence is included when the selection claim depends on measurable performance.

Feasibility probes are **pre-Blueprint nonproduction work** and do not violate the “no Product build before Blueprint approval” rule. They prove that a candidate engine is technically viable; they do not implement the Product module.

---

# 7. Schema alignment

The canonical schema registry SHALL add at least the following entities introduced by v0.11/v0.12:

```text
FoundryDecisionDossier
ProductBlueprint
ApprovalEnvelope
ProductApprovalAttestation
AnalysisAuthorizationProfile
RunEvent
RunStateSnapshot
EvidenceDependency
CleanRoomTransferManifest
FirstModuleCheckpoint
EnvironmentSnapshot
ArtifactRecord
BudgetAuthorization
ModelInvocation
SecurityFinding
LicenseDecision
ProductEngineCandidate
ProductEngineFeasibilityRecord
UntrustedRunnerProfile
ReleaseSignerRecord
FoundryEvaluationProtocol
FoundryEvaluationResult
```

All schema versions are immutable once referenced by a locked Blueprint, approval envelope, release record or trust certification.

---

# 8. Generalized evidence invalidation

Evidence invalidation SHALL NOT be limited to revoked tools.

## 8.1 Dependency graph sources

Every high-impact evidence/decision node records dependencies on applicable:

- tool ID + version/hash;
- model/runtime ID + version;
- prompt/template hash;
- SDK fingerprint database version;
- fixture/ground-truth version;
- policy bundle version;
- rights/authorization version;
- license classification;
- environment snapshot;
- source input hash.

## 8.2 Invalidation triggers

Examples:

```text
TOOL_REVOKED
MODEL_OUTPUT_CLASS_INVALIDATED
PROMPT_TEMPLATE_SUPERSEDED_FOR_DEFECT
FIXTURE_GROUND_TRUTH_CORRECTED
RIGHTS_AUTHORIZATION_REVOKED_OR_NARROWED
LICENSE_DECISION_CHANGED
SECURITY_POLICY_CHANGED
SDK_FINGERPRINT_INVALIDATED
INPUT_SIGNATURE_PROVENANCE_CHANGED
```

## 8.3 Propagation

The single-writer reconciler marks affected nodes using states such as:

```text
EVIDENCE_SUSPECT
RESULT_INVALID_PENDING_RETEST
DECISION_REQUIRES_RECONCILIATION
BLUEPRINT_REQUIRES_REVALIDATION
RELEASE_REQUIRES_RISK_REVIEW
```

A material suspect dependency reaching an approved/locked Blueprint raises:

```text
BLUEPRINT_INTEGRITY_ALERT
```

A released product additionally enters a disposition workflow. Possible human/policy-authorized outcomes include:

- continue with documented risk acceptance;
- quarantine distribution;
- rebuild/retest;
- hotfix;
- withdraw/supersede artifact;
- revoke release.

No automatic withdrawal or destructive action occurs without the governing release policy/human authority.

---

# 9. Stage outcome semantics

Run **state** and stage **outcome** are separate concepts.

Every optional/policy-sensitive stage records one of:

```text
PASS
FAIL
SKIPPED_NOT_APPLICABLE
SKIPPED_POLICY
BLOCKED_AUTHORIZATION
BLOCKED_ENVIRONMENT
BLOCKED_SECURITY_ENVIRONMENT
BLOCKED_BUDGET
INCONCLUSIVE
CANCELLED
```

Therefore a run SHALL NOT use `DYNAMIC_ANALYSIS_COMPLETE` or `BENCHMARKS_COMPLETE` to imply successful execution when the stage was skipped or blocked. A stage may be terminally recorded while its outcome explains what happened.

Add explicit paused states where applicable, including:

```text
PAUSED_MODEL_CAPACITY
PAUSED_REASONING_RUNTIME
PAUSED_CI_BUDGET
PAUSED_AUTHORIZATION
PAUSED_BLUEPRINT_REVOKED
PAUSED_USER_INTERVENTION
```

Canonical run states SHALL be validated against the error taxonomy during bootstrap so no state referenced by recovery logic is absent from the state schema.

---

# 10. Foundry quantitative evaluation protocol

The v0.11 initial quality targets remain **provisional lock-candidate targets**, but trust certification requires a pre-registered evaluation protocol rather than only threshold numbers.

## 10.1 Calibration vs holdout

- Calibration corpus may be used to improve rules/prompts/signatures.
- Locked holdout corpus SHALL NOT be used to tune the system after lock.
- Holdout membership/hash is frozen before the evaluated system version runs.
- Leakage/contamination checks are recorded.

## 10.2 Required protocol fields

```yaml
evaluation_protocol:
  taxonomy_version: ...
  supported_domains: [...]
  calibration_corpus_hash: ...
  holdout_corpus_hash: ...
  minimum_holdout_size: <frozen-before-evaluation>
  label_distribution_requirements: ...
  repeat_runs: >=3
  model_versions: [...]
  prompt_template_hashes: [...]
  scoring_rules: ...
  confidence_interval_method: ...
  partially_observable_policy: ...
  ground_truth_adjudicator: ...
  contamination_controls: ...
```

The exact minimum holdout size is **not invented in the architecture document**. It SHALL be determined and frozen for the supported pilot taxonomy before trust evaluation, with enough examples across required parent/sub-capability classes to make the declared metrics meaningful.

## 10.3 Hierarchical scoring

Evaluation distinguishes:

- parent capability correctness;
- sub-capability correctness;
- attribute correctness;
- overlap clustering correctness;
- blocked-vs-absent correctness;
- confidence calibration.

A correct parent with incorrect sub-capabilities is not scored as fully correct.

## 10.4 Semantic repeatability

LLM output need not be byte-identical. Repeatability measures semantic/decision stability after normalization to the structured schema.

## 10.5 Ground truth disputes

Disputed labels are resolved by a recorded adjudication process separate from the evaluated run. The holdout expected answer SHALL not be silently modified to make the current system pass; changes create a new holdout version and invalidate comparisons requiring the older ground truth.

---

# 11. Budget semantics: CI vs model/runtime vs storage/services

This section does not change the model-first philosophy and does not route work to tools merely to save tokens.

## 11.1 Default financial invariant

```yaml
paid_overage_authorized: false
```

No subsystem may silently convert quota exhaustion into a monetary charge.

## 11.2 Separate budget classes

Track separately where applicable:

```text
CI_COMPUTE
METERED_MODEL_RUNTIME
STORAGE
THIRD_PARTY_SERVICE
SIGNING/DISTRIBUTION
```

For a paid/unattended model adapter, record:

- provider/runtime;
- currency;
- billing period;
- per-run cap;
- cumulative cap;
- estimated reservation before execution;
- actual usage/spend;
- cancellation/pause behavior near the cap.

For non-metered interactive ChatGPT usage, AppFusion records **capacity/availability state**, not a fictitious currency cost.

## 11.3 Quota exhaustion

When a required resource is unavailable without unapproved spend, transition to the appropriate blocked/paused state and preserve state for resume. Do not silently degrade analytical quality solely to conserve model tokens.

---

# 12. Release signing and artifact promotion

## 12.1 `ReleaseSigner` principal

Release signing is a separate trust principal/environment from:

- Capability Foundry analysis;
- untrusted APK execution;
- ordinary Product build/test jobs;
- model/tool acquisition quarantine.

## 12.2 Requirements

- no signing keys in analysis or untrusted jobs;
- protected release environment;
- least-privilege, short-lived credentials where the signing/storage provider supports them;
- verified artifact promotion before signing;
- artifact hash/provenance/attestation recorded;
- branch/tag/release protection as configured;
- signing-key rotation and revocation procedure;
- explicit signed/approved exception record for security/license exceptions;
- release record links to Product Blueprint hash, Approval Envelope ID, test/security/license results and signed artifact hashes.

Signed/distributable/store-ready remain separate release states.

---

# 13. First-Module Checkpoint — confirmed normative behavior

The user explicitly accepted this design and it remains mandatory.

After the first approved module reaches its defined acceptance level, AppFusion SHALL publish a `FirstModuleCheckpoint` containing at minimum:

- module version/commit;
- Android screenshots/evidence;
- iOS screenshots/evidence when the approved target/platform scope requires them and the checkpoint test is applicable;
- automated test summary;
- contract conformance result;
- shared-core assumptions exercised;
- data/migration assumptions exercised;
- performance/resource observations;
- unresolved non-material risks;
- any emerging indication that the approved shared-core/module contract is wrong.

Default behavior:

```text
PUBLISH CHECKPOINT
      -> CONTINUE AUTOMATICALLY
```

The checkpoint SHALL NOT request approval and SHALL NOT pause by default.

It pauses only when:

- the user explicitly intervenes;
- a material Blueprint deviation is detected;
- a mandatory policy/security/authorization gate blocks continuation.

---

# 14. Tool Acquisition implementation staging — final decision

The prior S1 review is resolved deliberately as follows.

## Architecture

The full Tool Acquisition Engine remains part of AppFusion and remains specified in the locked architecture.

## Initial implementation

`FOUNDRY_VERTICAL_SLICE_ALPHA` does not require full autonomous discovery/search/quarantine/promotion orchestration before APK #1.

A missing capability during the initial slice produces a structured `MissingCapabilityReport` and may be resolved by the model/operator using the same security policy and provisional Tool Registry concepts.

## Expansion

Full autonomous:

```text
DISCOVER -> EVALUATE -> QUARANTINE -> VERIFY -> PROVISIONAL_USE -> PROMOTE/REVOKE
```

is implemented in the Foundry expansion based on actual capability gaps encountered.

This is implementation sequencing, not removal of the capability.

---

# 15. Tool/readiness tiers — interpretation

Tool tiers describe readiness/installation and security maturity, not a prohibition on model-selected use.

Indicative classes:

### `CORE_READY`
- JADX
- apktool
- Androguard
- apksigner
- Android SDK/ADB/emulator
- JDK/Gradle
- schema validation

### `OPTIONAL_READY`
- Maestro/Appium as needed
- MobSF
- Syft/Trivy/Grype/Gitleaks
- benchmark libraries

### `ADVANCED_LAB`
- Frida/Objection
- mitmproxy
- Ghidra/LIEF/Rizin
- Joern
- ScanCode/ORT
- Graphify

### `ACQUIRED_DOMAIN_SPECIFIC`
- capability/domain engines discovered later

If an Advanced Lab tool is necessary on APK #1 and the authorization/security lane permits it, the model may use it. The tier does not force inferior analysis.

Every tool record SHALL pin exact upstream identity, version/commit, license, integrity/provenance, installation recipe and current verification date.

---

# 16. Final lock-candidate status

After this errata is incorporated, the remaining major uncertainty is empirical rather than architectural.

The next canonical version SHALL be:

```text
APPFUSION COSCIENTIST SYSTEM BLUEPRINT v1.0 LOCKED
```

only after a final consistency check confirms that:

1. v0.11 + v0.12 contain no unresolved normative contradictions;
2. all schema/state names used by policy/workflows are declared;
3. the three-artifact approval model is reflected consistently in repository layouts and gates;
4. Alpha/Trusted/Product/System release labels are not conflated;
5. iOS acceptance matches the approved platform scope;
6. untrusted workflow controls are implementable/testable in the selected execution environment;
7. no reviewer recommendation has silently overridden the user-fixed requirements.

The subsequent implementation target is **`FOUNDRY_VERTICAL_SLICE_ALPHA`**, not another broad architecture redesign.

---

# 17. Reviewer disposition record

## Final Codex v0.11 review

| Finding | Disposition | Reason |
|---|---|---|
| Three clean-room/approval artifacts | ACCEPT | Removes genuine canonical-artifact ambiguity and strengthens information separation. |
| Alpha vs trusted Foundry v1 | ACCEPT | v0.11 contained a real milestone naming contradiction. |
| Mandatory iOS for Android+iOS Blueprint | ACCEPT | Cross-platform Product v1 cannot truthfully pass without iOS build/test. |
| Machine-verifiable hostile runner profile | ACCEPT WITH PLATFORM-SPECIFIC IMPLEMENTATION | Security claims should be executable/tested. GITHUB_TOKEN is permission-disabled rather than falsely claimed nonexistent. |
| Separate IR vs UA system release labels | ACCEPT | Ultimate unattended objective should not be implied by an IR-only demonstration. |
| Product Engine Feasibility Gate | ACCEPT STRONGLY | Prevents untested documentation-level engines from being frozen into a Blueprint. |
| Schema alignment | ACCEPT | Mechanical consistency requirement. |
| Generalized evidence invalidation | ACCEPT | Evidence provenance already supports broader dependency invalidation. |
| Skipped-stage outcomes | ACCEPT | Prevents “complete” from meaning “successfully executed.” |
| Stronger quantitative protocol | ACCEPT WITH CONFIGURED SAMPLE SIZE | Exact holdout N must be empirically justified/frozen rather than invented in architecture prose. |
| Separate model and CI budgets | ACCEPT WITH PHILOSOPHY PRESERVED | Needed for unattended paid runtimes; not a token-saving routing rule. |
| Release signing hardening | ACCEPT | Correct trust-boundary improvement. |

## Prior Claude v0.10 closure review

- N1 zero-cost billing hard stop: already accepted and retained.
- N2 revoked-tool evidence invalidation: accepted and generalized in this errata.
- N3 canonical paused state: accepted and expanded into state/outcome consistency.
- S1 Tool Acquisition sequencing: accepted as staging, not removal.
- S6 First-Module Checkpoint: accepted as mandatory non-blocking report.

---

**End of v0.12 Lock-Candidate Errata**
