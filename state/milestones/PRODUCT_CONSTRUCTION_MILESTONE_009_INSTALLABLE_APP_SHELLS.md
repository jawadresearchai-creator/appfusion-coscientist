# Product Construction Milestone 009 — Installable App Shells

Application: `docvault-lasttime-fusion`

Occurred at: `2026-09-03T11:33:33Z`

## Outcome

The Product repository now contains real Android and iOS application projects around the proven shared Document Vault core. Product PR #2 merged at `b1ccbd1b56bbd06a178d9f97a7209a8c154376d4` after Product Boundary CI run `33749114150` and Product Construction CI run `33749114136` passed.

This milestone meets the Delivery Orchestration v1.1 deadline for the first installable artifact. It does not claim that Journey J1 or the release train is complete.

## Artifact evidence

- Android artifact `9890952602` contains `androidApp-debug.apk`, SHA-256 `9398df8ab497ffa6ef309bd2b6ef5638143c8877f75a8e27e694a8a7628a5ffb`.
- The same Android artifact contains `androidApp-release-unsigned.apk`, SHA-256 `d66d256040fe0ca9263431a734d08a54d8dc8312a996eacc5db0aaf5e06ee4f8`.
- The same Android artifact contains `androidApp-release.aab`, SHA-256 `e3e6d86e470d24b323e01654232fba3404b93694dbc4093be8f60f7110838b50`.
- iOS artifact `9891032519` contains `AppFusion-ios-simulator.zip`, SHA-256 `e85d797d93d3ce417e411eb551b77c3c81a2ea56128ab2fd8f013aff34eca4d7`.

The Android debug APK and iOS Simulator app are marked `PASS` as build artifacts. The Android release APK and AAB remain `IN_PROGRESS` because they are unsigned and have not passed distribution/install validation.

## Gate evidence

- Shared JVM and Android build contracts passed.
- Android Keystore device probe passed on a provisioned emulator.
- Apple Keychain adapter passed from a simulator-installed signed host.
- The iOS Simulator application shell built and uploaded.
- The clean-room Product Boundary guard passed.
- The initial Android application compile failure was repaired once by adding the public Room/SQLite ABI dependencies. This was repair attempt 1 and the repeated run passed.

The redundant post-merge construction run was cancelled after the GitHub API showed that the tested PR merge commit and final merge commit had the identical tree `c2a302289e4f7590bc6b399d4abf26b99effd9fa`. This preserves CI budget without reducing evidence coverage.

## Remaining truth

- The Android app has not yet completed installed Journey J1 UI automation.
- The iOS UI currently proves its secure host integration but does not yet expose the full J1 document workflow.
- Android distribution signing credentials are not configured.
- J2 and J3 have not started.
- Final source ZIP, test/security reports, screenshots, checksum manifest, and release packaging remain outstanding.

## Next safe action

Install the Android debug APK in the CI emulator and automate J1 through create, restart, search, and reopen. Then wire and validate the same J1 workflow in the iOS Simulator. Build evidence alone must not be promoted to journey-complete evidence.
