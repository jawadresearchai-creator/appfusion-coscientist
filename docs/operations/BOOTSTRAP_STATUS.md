# Bootstrap Status

## Provisioned

- Private Capability Foundry repository.
- Private Product Foundry repository.
- Private Google Drive root and intake/report/blueprint/release/audit folders.
- Cloud-authoritative environment manifest.
- Contract and policy validation package.
- Initial schemas for intake, authorization, events, outcomes, dossiers, blueprints, approvals, approval events, attestations, and untrusted runner policy.
- Trusted Foundry CI and request-registration workflow.
- Explicitly blocked untrusted analysis workflow.
- Clean-room Product repository guard and CI.
- Optional local mirrors with GitHub remotes.
- Drive-first project registry and versioned `ApplicationState`/`SessionBootstrap` contracts.
- Deterministic zero/one/multiple active-app selection for new sessions.
- Essential-only GitHub routing, path-filtered CI, and cancellation of superseded runs.

## Current resumable state

- Registry revision: `2`.
- Active Product applications: `0` (no Product Blueprint has been approved).
- Next safe action: register the first rights-authorized APK after the Drive-to-CI identity and untrusted static-runner gates are satisfied.
- Portable new-chat instructions: `docs/operations/NEW_CHAT_BOOTSTRAP.md` and the matching file in Drive `00_CONTROL`.

## Blocked before APK #1

- `DRIVE_READER_IDENTITY`: requires Google workload identity or another approved cloud storage bridge.
- `UNTRUSTED_STATIC_RUNNER_ATTESTATION`: requires an isolated analysis image/lane with tested network and metadata denial.
- `RIGHTS_ATTESTATION`: supplied per APK through the intake request.

## Not required for initial bootstrap

- Release signing secrets.
- Apple Developer credentials.
- Full autonomous Tool Acquisition.
- Persistent metered-model coordinator.
- A local Android SDK or local emulator.
