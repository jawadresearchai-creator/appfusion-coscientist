# Authorized public Product execution — 2026-09-04

## Authority and privacy boundary

The user requested that Drive remain private while Android and iOS use public
GitHub builds, then answered **"yes i authorize"** to the explicit question about
publishing Android/iOS source, tests and workflows in a new public repository.
This is not approval to publish input APKs, decompilation, dossiers, credentials,
private documents, old repository history or private Drive identifiers.

- Active Product: https://github.com/jawadresearchai-creator/appfusion-product-public
- Authoritative private control: `jawadresearchai-creator/appfusion-coscientist`
- Historical private Product: `jawadresearchai-creator/appfusion-product`
- Drive remains the private input/report store and cloud-state projection.

The public repository starts a fresh history at
`14a3141a614a69fadfdf242894101f44a868164c`. Its allowlisted snapshot came from private
Product commit `6856c437c1f8c3dad4effbfa7fa230e9efb21201`; 52 runtime/build files were
byte-identical. Only approved blueprint/attestation, Product runtime, build/test
code and sanitized operational files were included. Old history, private docs,
Drive identifiers, generated evidence, binaries and credentials were excluded.
ProductBlueprint SHA-256 is unchanged:
`2120f5989ec35562377bd42e032018bd0004916d5ea4c56005f8e7048414b6fc`.

Public-source checks enforce the allowlist and reject known secret/private-input
patterns. These checks supplement review; they are not proof that a scanner can
recognize every secret. Every future public change still needs this boundary check.
No additional open-source license grant was invented from publication permission.
This document contains private provenance and must never be copied to Product.

## Zero-new-charge execution boundary

Only standard public `ubuntu-24.04` and `macos-15` jobs may execute. The job guards
check the exact public repository and reject private/fork contexts before runner
allocation. No larger runner, paid service, overage, monthly-tier substitute,
private checkout, private-source proxy or Drive credential is configured.
The original seven private workflows remain disabled; do not re-enable them.
There is one public preflight/build workflow, avoiding the duplicate boundary run.
Platform impact selection and bounded timeouts remain; Gradle caches are disabled
and temporary CI artifacts expire after three days. Public Releases hold the
durable public development binaries, source archive, report and checksums.

GitHub currently lists standard public-hosted Actions usage as free. This removes
the private monthly build-minute dependency, not all operational limits or the
possibility of future provider-policy changes. Never react to a restriction by
enabling billing. No assertion is made about unrelated existing account charges.
Free-execution evidence is scoped to this workflow's free service category, not a
claim that the entire GitHub account has no payment method.

- https://docs.github.com/en/billing/concepts/product-billing/github-actions
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job
- https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases

## Delivery and continuation

The available downloads are development artifacts, not final release acceptance.
The APK published as tested must match the SHA-256 from the installed Android J1
evidence, not merely another build of the same commit. The iOS Simulator ZIP is
for an Apple Silicon Mac's Xcode simulator, not an IPA installable on an iPhone.
Do not buy signing or distribution services; those remain outside the free scope.

Read the event tail for the actual public CI run, release URL and test outcome.
Once free execution is verified, continue iOS J1, then J2/J3 and release/security
gates. Do not restart the executor-design discussion or request publication
permission again for this approved Product snapshot. ChatGPT web remains a
resumable control surface; public CI does not create unattended AI reasoning.
