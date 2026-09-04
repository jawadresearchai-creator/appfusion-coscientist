# Product Construction Milestone 011 — Cross-platform J1 verified

Application: `docvault-lasttime-fusion`
Recorded at: `2026-09-04T08:25:40Z`
Canonical revision: 23

## Outcome

The installed Android and iOS simulator applications passed the encrypted-document create/restart/search/decrypt/reopen journey. PR #2 was fast-forward merged at `1c6ab92f25a281a6776c7899645917d21695765f`. Both candidate CI 33836151702 and the resulting main CI 33837384267 passed all four jobs.

The exact tested APK and simulator application, public source ZIP, both platform evidence bundles, test report and SHA-256 manifest are available in [development release dev-j1-20260904](https://github.com/jawadresearchai-creator/appfusion-product-public/releases/tag/dev-j1-20260904). All seven uploaded digests and anonymous download-page access were verified. The iOS ZIP's embedded executable was also verified against the hash recorded by the installed test harness. Both reopened-document screenshots were visually inspected.

## Evidence-based repairs

- Keyboard-aware iOS layout and accessible Done action fixed a keyboard-obscured Search failure.
- The named installed XCTest is now an explicit step in the existing authorized workflow, with result-bundle/log retention and exact tested-application packaging; recursive Xcode build-phase testing was removed.
- Mutable shared vault calls and closure are serialized, with a source regression check.
- Android handles at most one precisely identified Pixel Launcher system ANR; application crashes/ANRs are not dismissed. Neither accepted candidate/main run required this recovery.
- Twenty-four Product boundary/harness tests passed. Android runtime tests, shared Android/iOS contracts and installed native-key security probes passed. iOS installed J1 reports one passed, zero failed and zero skipped.
- Original failing run 33834830361 is retained as failure evidence. Superseded run 33835978203 was cancelled, not accepted as a pass.

## New concurrent-writer conflict — do not lose J1 progress

After the verified main build, a separate writer added `.github/workflows/aleil-ios-test.yml` again at `c78b82beae06c194a77a4256610150689ea97447`. Its [Product CI 33838952381](https://github.com/jawadresearchai-creator/appfusion-product-public/actions/runs/33838952381) failed preflight: there are now two hosted workflows and the additional job lacks the required public-repository allocation guard. Its runner input is unrestricted.

The later commit changes only that workflow, not the accepted application source. It was not overwritten. The public development release is pinned to the preceding verified source and does not claim the later main revision passed. The committed application/registry and delivery plan now preserve J1 PASS while pausing further construction for user direction and concurrent-writer coordination. This is a workflow-ownership conflict, not a new cryptographic or J1 implementation failure.

## Privacy, cost and release boundary

Drive and both original repositories remain private. All seven original private workflows remained disabled when checked. No billing, paid service, private CI reactivation or local build dependency was introduced by this work.

Android is a tested debug build; use disposable data and do not uninstall a valuable earlier installation to resolve a debug-signature mismatch. iOS is an arm64 simulator app, not a physical-iPhone IPA. J2, J3, final security review and distribution/signing acceptance remain unfinished. Final release readiness is false.

## Resume

Obtain direction on the independently re-added ALEIL workflow and coordinate a single writer. Restore the approved single guarded standard-public workflow or seek explicit approval for a different design; do not weaken the guard just to make CI green. Verify the reconciled revision without discarding accepted J1 evidence. Then implement J2 activity/cadence/reminders/restart/timezone behavior, J3 links/search and final gates. Do not restart J1 or repeat public-source authorization.

Git event 23 is authoritative; update existing Drive application state and delivery-plan files after the valid Git commit, then registry last. Preserve their IDs, parents and private sharing.
