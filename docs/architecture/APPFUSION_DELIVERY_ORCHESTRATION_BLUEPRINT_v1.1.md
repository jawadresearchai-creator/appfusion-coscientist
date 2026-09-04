# AppFusion CoScientist
## Delivery Orchestration Amendment — v1.1

**Authorized:** 2026-09-03  
**Authority:** user-approved correction to the v1.0 locked system blueprint  
**Scope:** orchestration, state integrity, delivery closure, CI efficiency, and release convergence  
**Product behavior authority:** the exact approved ProductBlueprint remains unchanged

## 1. Purpose

The v1.0 blueprint established the correct security, authorization, clean-room, modularity, and cross-platform boundaries. This amendment closes the operational gaps that allowed valid infrastructure checkpoints to advance without forcing an installable product and allowed more than one interactive operator to hold writable stale state.

This amendment does not claim that governance by itself creates a finished-application factory. A working AppFusion CoScientist requires four independently testable capabilities:

1. a safe, resumable state coordinator;
2. evidence-producing APK intelligence and capability selection;
3. release-bound Product construction with installable Android/iOS shells and end-to-end journeys;
4. a persistent reasoning coordinator for unattended work after every chat is closed.

AppFusion may call itself `INTERACTIVE_RESUMABLE` when items 1–3 operate through ChatGPT web or Codex. It may call itself `UNATTENDED_AGENTIC` only after item 4 is deployed and its leases, budgets, credentials, and interruption recovery are demonstrated.

## 2. Corrected state authority

Small control state is authoritative in the private Capability Foundry Git repository because Git supplies atomic commits, immutable history, fast-forward conflict rejection, and inexpensive cross-surface reads. Google Drive remains the authoritative store for bulky source inputs, private reports, screenshots, videos, release copies, and other non-Git artifacts.

The state model is:

`immutable RunEvents -> ApplicationState projection -> ProjectRegistry summary`

Rules:

1. A material transition is one Git commit containing the new event, affected `ApplicationState`, registry projection, and any changed delivery plan.
2. Every transition declares the expected registry revision, expected application-state revision, and next event sequence.
3. A stale expected revision fails; it never overwrites a newer state.
4. One application-scoped writer lease is held while a transition is prepared and promoted.
5. Drive copies are projections. They never outrank a later valid Git event merely because their modification timestamp is later.
6. Drive projections record the Git commit and event hash that produced them.
7. A new session reads the Git registry and event tail first, then verifies any Drive projection against the same revision and hash.
8. Milestone prose is generated evidence, not state authority.
9. Missing or non-contiguous events fail state validation.
10. Existing v1.0 state is migrated without deleting historical Drive revisions or local uncommitted evidence.

## 3. Release-train scope lock

The active release train is `DOCVAULT_LASTTIME_V0_1_INSTALLABLE`.

Included:

- encrypted Document Vault create/import, persistence, restart, local search, and reopen;
- LastTime activity creation, completion history, last-completed state, and one deterministic reminder path;
- a typed document/activity link and federated search result;
- Android installable application shell;
- iOS simulator-installable application shell;
- source archive, tests, reports, screenshots, and checksums.

Deferred until the first installable train passes:

- live camera scanner;
- OCR and structured extraction;
- PDF editing/export workbench;
- memory graph expansion;
- cloud/account sync;
- office-suite capabilities;
- additional unrelated application ingestion;
- advanced document modes;
- signed App Store/TestFlight distribution unless credentials are separately authorized.

A unique discovered capability is no longer automatically inserted into the active release. It is classified as `INCLUDE_CURRENT_TRAIN`, `REPLACE_INCUMBENT`, `COMBINE`, `BACKLOG`, `REJECT`, or `INCONCLUSIVE` using product coherence, user value, security/privacy risk, cross-platform feasibility, cost, and dependency impact.

## 4. Mandatory user journeys

The first release train is not complete until all required journeys have reproducible evidence.

### J1 — Encrypted document survives restart

Create or import a document, encrypt and persist its payload and metadata, terminate the process, restart on Android and iOS, rebuild authorized search, find the document, and reopen verified plaintext.

### J2 — LastTime cadence survives rescheduling

Create an activity, record completion, calculate last-completed and next-due state, schedule a reminder, restart/reconcile transport, and preserve deterministic state across timezone fixtures.

### J3 — Cross-domain link and search

Link an activity to a document through typed opaque IDs, emit an activity event, and return authorized document and activity results through federated local search without joining domain databases.

## 5. Artifact-first milestone law

1. No more than two consecutive infrastructure-only milestones are allowed.
2. Milestone 009 is the latest permissible point for the first Android APK and iOS simulator app artifact.
3. Every subsequent milestone must advance at least one required journey, required deliverable, or release-blocking defect.
4. Three consecutive milestones without a new user-visible artifact or journey transition force `DELIVERY_SLICE_REQUIRED`.
5. A checkpoint may not select another audit as its next action unless new evidence invalidates the last audit.
6. A failure signature receives at most two autonomous repair attempts. The third occurrence pauses with evidence and a bounded decision request.
7. Optional features cannot block the active release train.
8. A passing library test is not an application acceptance result.

## 6. Product module boundaries

The single `:shared` bootstrap module is transitional. Before the second domain is substantially implemented, Product code must establish enforceable boundaries for:

- core contracts;
- security and encrypted payloads;
- document-vault domain;
- activity/cadence domain;
- scheduling transport;
- federated search;
- backup coordination;
- Android application;
- iOS application.

Platform adapters depend inward on contracts. Domains do not access each other's database rows. Shared verification operations such as authenticated document-blob reading must have one implementation and typed failure results.

## 7. CI tiers and budget enforcement

CI stages are:

- `TIER_0`: clean-room, schema/state integrity, compile, and JVM/shared tests;
- `TIER_1`: changed platform adapter tests;
- `TIER_2`: Android emulator and iOS simulator acceptance after Tier 0 passes;
- `TIER_3`: release matrix, SBOM, security/license gates, provenance, packaging, and checksums.

Rules:

1. Expensive construction jobs depend on a passing clean-room/preflight job.
2. Platform jobs use path/impact selection where correctness permits.
3. Unchanged failed jobs may be rerun; code changes create one batched checkpoint rather than a series of speculative main-branch pushes.
4. CI dispatch requires verified free-only execution and zero new service charges. Billing activation, paid services, overages and payment requests are prohibited. Monthly free tiers are not a permanent solution. See `docs/operations/FREE_ONLY_EXECUTION.md` (2026-09-04 user correction).
5. GitHub usage records runner/job minutes separately for Linux, Android emulator, and macOS.
6. Direct pushes of unverified construction to `main` are prohibited. A candidate branch is tested, then promoted by fast-forward only if the expected base still matches.

## 8. APK intelligence closure

ZIP inventory is intake validation, not feature intelligence. The Foundry is complete only after it can, within the authorized lane:

- reconstruct and recursively inspect APK/APKM/XAPK split packages;
- decode manifests and resources;
- decompile DEX for static understanding;
- inventory native libraries, SDKs, databases, components, permissions, navigation, storage, and network indicators;
- produce evidence-addressed capability records;
- classify overlap and uniqueness;
- execute objective benchmarks where claims are benchmarkable;
- keep blocked, absent, and inconclusive results distinct;
- emit a strict ProductBlueprint without source identity leakage.

Dynamic comparison remains blocked until a disposable runner proves the required isolation. Static evidence alone cannot establish runtime quality superiority.

## 9. Approval and clean-room closure

1. Approval attestations must be verifiable against an authenticated external identity or signed event, not only an `APPROVED` string.
2. Product transfer validates strict nested schemas, exact bytes, policy version, approval status, and revocation/supersession state.
3. Leakage checks inspect keys, values, filenames, commit-introduced paths, and declared fixtures.
4. Product-facing artifacts use product identities only. Foundry application/source identifiers are forbidden.
5. Critical engine feasibility, license, security/maintenance, platform, and benchmark records are durable structured artifacts.

## 10. Release terminal condition

The active release train reaches `RELEASE_CANDIDATE` only when:

- all required journeys pass;
- Android debug APK and release candidate APK/AAB exist;
- the iOS simulator app builds, installs, launches, and passes required journeys;
- signed iOS archive state is explicitly `PASS`, `BLOCKED_AUTHORIZATION`, or `DEFERRED_BY_RELEASE_SCOPE`;
- zero known critical security or data-loss defects remain;
- required migration/restart tests pass;
- dependency, license, SBOM, and provenance evidence exists;
- source ZIP, test report, security report, screenshots, and checksums exist;
- every artifact is bound to the ProductBlueprint hash and source commit.

`RELEASED` requires promotion to GitHub Releases and the approved Drive release folder. A library-only checkpoint can never satisfy this condition.

## 11. Persistent autonomy

Interactive ChatGPT web and Codex sessions may plan, reason, repair, and promote work while active. Closing all sessions stops model reasoning.

True unattended execution additionally requires:

- a persistent coordinator service;
- durable task queue;
- application leases and heartbeats;
- authorized GitHub App/service identity;
- approved Drive/object-storage identity;
- a reasoning runtime requiring no new service charge (paid metered APIs are not authorized);
- retry classification and dead-letter handling;
- approval/deviation enforcement;
- demonstrated interruption recovery.

Until this is deployed, the truthful label remains `INTERACTIVE_RESUMABLE_DELIVERY_CONTROLLED`.

## 12. Immediate implementation order

1. Migrate state to revisioned Git-backed event/projection contracts and close missing events 015–016.
2. Register this amendment, its independent audit, and the v0.1 DeliveryPlan as event 017.
3. Update new-chat bootstrap and stale status documentation.
4. Add state-integrity tests and stale-writer/lease tests.
5. Create Android and iOS application shells and produce the first installable CI artifacts.
6. Connect Journey J1 to the existing Document Vault foundation.
7. Implement the bounded Activity/Cadence core and Journey J2.
8. Implement typed cross-domain linkage and Journey J3.
9. Complete release, security, license, and provenance gates.
10. Resume deferred scanner/OCR/PDF capabilities after the first installable train.
