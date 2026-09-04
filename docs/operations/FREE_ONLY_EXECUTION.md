# Free-only correction — 2026-09-04

The user's rule is no billing and no paid services. It is not merely a request to
stay below an approved spend cap. Monthly free tiers are not a permanent solution.
This rule supersedes earlier statements inviting metered budgets, paid signing,
or restoration of paid capacity. No billing or payment method was enabled by
this correction. No claim is made about unrelated existing account charges.

## Enforced now

- BudgetAuthorization rejects paid_overage_authorized=true and nonzero caps.
- Policy and both repository manifests require FREE_ONLY and zero new charges.
- All seven AppFusion GitHub hosted workflows are disabled at the provider.
  Every job also has an exact-commit free-only pre-allocation guard.
- Free-execution admission rejects missing/stale evidence, unapproved access,
  billing, overage, unknown providers, monthly-tier substitutes, larger/private
  runners, and disguised public proxies for private builds.
- Optional local checks run without GitHub Actions or a new service account.
- No public repository, new CI account, or new third-party source access was created.

Provider evidence is an operator responsibility, not something these scripts
can fabricate. The validator checks evidence shape and constraints; it does not
query billing or prove that a provider receipt is authentic. Disabled workflows
are the current safety stop; skips cannot count as passed tests.

## Remaining choices

Public Product source with standard GitHub runners is currently free without a
monthly build-minute allowance. Publishing is a material privacy/licensing
decision requiring explicit approval and review of the exact source set and
history first. Keep Foundry analysis, input APKs, documents, keys and Drive private.
Do not make a public workflow a proxy for unrelated private builds. Account-level
restrictions may still apply, and no vendor policy is a forever guarantee.

Existing authorized hardware has no CI-service charge or monthly compute quota,
but still has hardware, electricity and maintenance costs. Android can use the
existing Windows adapter. iOS requires an existing authorized Mac. Making that
required would change the cloud-first/no-local-dependency requirement.

No verified executor currently satisfies private, cloud-only, quota-independent,
and zero-service-charge macOS execution together. Preserve accepted Android
artifacts while requesting the missing publication/hardware decision, not payment.

## Google Drive

Drive is storage: retain inputs, checkpoint projections, artifacts and evidence.
It cannot run Gradle, Xcode or simulators. Apps Script is a separate quota-limited
runtime, not an OS build host. Colab is separate, limited interactive compute and
is not a permanent unattended CI substitute. Codemagic was investigated but its
monthly allowance was rejected; no connection or build was made.

## Evidence and sources

Run `pytest -q`, `appfusion bootstrap-check`, and `appfusion orchestration-check`
on the existing optional adapter. Public-source execution remains unauthorized.
`appfusion free-execution-check <evidence.json>` must pass before any future
admission; do not set APPFUSION_FREE_APPROVED_SHA from repository assertions alone.

- [Standard public GitHub runners](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job)
- [Drive storage API](https://developers.google.com/workspace/drive/api/guides/about-sdk)
- [Apps Script quotas](https://developers.google.com/apps-script/guides/services/quotas)
- [Colab limits](https://research.google.com/colaboratory/faq.html)
