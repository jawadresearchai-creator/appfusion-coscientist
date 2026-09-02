# Drive-to-CI Workload Identity Gate

This gate supplies the trusted intake coordinator with short-lived read-only Google Drive access. It does not grant any Drive credential to the untrusted static-analysis container.

## Required external configuration

Provision Google Workload Identity Federation for GitHub Actions and a dedicated Google Cloud service account. Restrict the provider to `jawadresearchai-creator/appfusion-coscientist` and preferably `refs/heads/main`. Grant the GitHub federated principal `roles/iam.workloadIdentityUser` on that service account. Do not create or store a service-account JSON key.

Share only the dedicated AppFusion private intake workspace, or the exact staged intake files, with the service-account email as a Drive reader. Do not share the user's entire My Drive.

Set these GitHub repository variables (they are identifiers, not credentials):

- `APPFUSION_GCP_PROJECT_ID`
- `APPFUSION_GCP_WIF_PROVIDER` — full `projects/<number>/locations/global/workloadIdentityPools/<pool>/providers/<provider>` name
- `APPFUSION_GCP_DRIVE_READER_SERVICE_ACCOUNT` — dedicated service-account email

The trusted workflow `.github/workflows/trusted-drive-package-intake.yml` uses the pinned `google-github-actions/auth` action with GitHub OIDC and requests only the `https://www.googleapis.com/auth/drive.readonly` scope. The generated access token exists only in the trusted retrieval step.

## Acceptance

The gate may be closed only after a real authorized request proves all of the following:

1. WIF authentication succeeds without a stored service-account key.
2. The trusted coordinator downloads only the SourceBundle-bound Drive file IDs.
3. Every single file or chunk matches its declared byte size and SHA-256; chunked packages also match the logical reconstructed size and SHA-256.
4. The untrusted container re-proves network denial, metadata denial, and absence of sensitive environment before parsing.
5. The verified package is passed read-only into the attested static container without the Drive access token.
6. Durable evidence contains only retrieval/hash records, sandbox evidence, and normalized static inventory; APK/APKM bytes are destroyed before artifact upload.
7. Missing, expired, or unauthorized identity fails closed as `BLOCKED_AUTHORIZATION`.

Dynamic/emulator execution is not enabled by this gate.
