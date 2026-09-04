# Product Construction Milestone 012 — Android activity UI preview

Application: `docvault-lasttime-fusion`

Canonical revision: 26

Recorded: `2026-09-04T17:17:24Z`

## Delivered

The existing Android app now has an Activities & cadence screen backed by the accepted shared activity repository and its separate Room database. Installed tests prove invalid-input handling, activity creation, completion count/history, process restart, device-timezone change and reopening history. The screen explicitly states that native notifications are not yet connected.

The [development release](https://github.com/jawadresearchai-creator/appfusion-product-public/releases/tag/dev-android-activity-20260904) contains the exact tested APK, public-only source ZIP, compact current and superseded test evidence, report and checksums. All five uploaded SHA-256 digests were verified. The final activity screenshot was visually inspected. Existing J1 development releases and revision-23 evidence were not changed.

Product source: `0f5d69ec2d71a5c43aea2b7d05a27aa88e0bc90c`

APK SHA-256: `659f30e4698d60fa9a36ea4d9790404e4c3219f695eb0ade27ba81e92127890b`

Source ZIP SHA-256: `bbb0d409c628d8927a2e859b6f1e9fb85cf2fa5cb7cfef57ac678b486f910363`

## Evidence and one bounded repair

- Initial PR #4 / `14c05a8`: candidate 33894966082 passed all four jobs.
- First main 33896246998 passed JVM/Android build, Keystore/J1 and iOS shared/framework/Keychain/installed J1. Overall it FAILED because the Android J2 driver tapped a clipped history-button target at y=799 on an 800-pixel display. The failure screenshot showed the keyboard; completed-count and timezone assertions had already succeeded.
- PR #5 / `0f5d69e` rejects screen-edge targets so the existing driver scrolls them into the usable viewport. An exact clipped-vs-visible regression test was added. Application source, journey assertions, timeouts and workflow guards were not changed by this repair.
- Repair candidate 33897363864 and [resulting main 33898157632](https://github.com/jawadresearchai-creator/appfusion-product-public/actions/runs/33898157632) passed preflight and the affected Android device job, including J1 and J2 activity UI. Neither accepted repaired activity run needed emulator-recovery actions. Both synthetic candidate merge trees were verified equal to their selected source trees before fast-forward promotion.
- All 28 Product boundary/harness checks pass. Unchanged JVM/iOS jobs in the repair runs were SKIPPED, not fresh passes; their successful evidence is retained at `14c05a8`. The only successor differences are the Android test driver and its test file.
- The final downloaded APK digest matches both final-main Android test receipts. Evidence/report explicitly distinguish this UI slice from complete J2 acceptance.

## Remaining work and safety

J1 and J2 shared contracts remain PASS. J2 and its Android criterion remain IN_PROGRESS; iOS J2 UI is NOT_STARTED. Implement native notification permission, delivery, deduplication and boot/timezone reconciliation, plus iOS activity UI, before accepting J2. Then finish J3, final security/UX/accessibility checks and signing/release gates. The early cadence form needs persistent field labels and broader usability review before final release.

This is a debug Android preview for disposable test data. A CI debug-signature change may prevent upgrading an older build; do not uninstall valuable data merely to resolve that mismatch. No physical-iPhone IPA, paid distribution service or final release is claimed.

No Project B/ALEIL repository or Drive state was accessed. The single guarded standard-public workflow is preserved and extended only with the Android test/evidence step and path classification; its current blob is `6e1ded151a39f43ea81e8b02655ef9262ebaa348`. No billing, paid service, private CI reactivation or mandatory local executor was introduced. The existing private Drive files must be projected in place after this valid Git transition, registry last.
