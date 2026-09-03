# Product Construction Milestone 004 — Document Vault Core Checkpoint Locked

Application: `docvault-lasttime-fusion`

Blueprint SHA-256: `2120f5989ec35562377bd42e032018bd0004916d5ea4c56005f8e7048414b6fc`

Milestone: `DOCUMENT_VAULT_CORE_CHECKPOINT_LOCKED`

Occurred at: `2026-09-03T05:04:00Z`

## Decision

Lock the first bounded shared `document_vault` checkpoint. It composes Room3 document metadata with immutable, revision-addressed SecureBlob payloads through product-owned repository contracts. The checkpoint covers encrypted create, authorized read, encrypted update, idempotent archive, authorized search projection, append-only activity events, and versioned encrypted backup-record export.

This locks shared lifecycle behavior and the Room metadata schema only. A production filesystem-backed `SecureBlobStore`, crash-recovery protocol, durable search/event outbox, restore coordinator, UI, camera, OCR, PDF export, and secure sharing remain outside this checkpoint.

## Evidence

Final Product commit: `8076430eaa1b4d32d49c604c0f2d9b3b2bba3fd8`

- Product Boundary CI run `33716941887`: PASS.
- Product Construction CI run `33716941898`: PASS.
- Android/JVM shared build and contract suite: PASS.
- Android API 35 Keystore runtime probe: PASS.
- iOS Simulator ARM64 shared contracts, framework link, and Xcode-hosted Keychain probe: PASS.

The cross-platform contract suite proves:

1. Room metadata and encrypted payloads remain separated.
2. Create/read/update round trips never persist plaintext in the blob record.
3. Each update writes a new revision-addressed encrypted blob before the metadata pointer changes.
4. A failed metadata commit removes the staged blob, preserves the previously readable revision, and emits no event.
5. A successful update collects the superseded encrypted blob.
6. Unauthorized read, search, and backup export return no document.
7. Archive removes the document from search and emits the expected append-only lifecycle event.
8. Backup export preserves the encrypted payload in a strict versioned record and rejects corrupted integrity bytes.
9. Room schema version 1 migrates through versions 2 and 3; deliberate version 1→2 and version 2→3 failures roll back schema and data atomically.
10. SecureBlob caller context authenticates the blob identity and content type, rejecting ciphertext reassignment under a different document context.
11. Legacy pre-vault rows are preserved but marked `LEGACY_MIGRATION_REQUIRED`, preventing them from being treated as valid encrypted vault records.

## Review correction

The first implementation commit `97133941cb1f364206c41e1cbdcfb2b471314a62` passed Product Boundary CI run `33716493493` and Product Construction CI run `33716493388`. Pre-lock review found that the encrypted envelope authenticated its own key metadata but was not yet bound to the owning document/blob identity. Commit `8076430eaa1b4d32d49c604c0f2d9b3b2bba3fd8` added bounded caller context to AES-GCM associated data and explicit legacy-row fail-closed handling. Only the hardened commit is locked.

## Next safe action

Implement replaceable Android and iOS filesystem-backed `SecureBlobStore` adapters using same-directory temporary writes, durable flush where supported, atomic replacement, startup recovery, path traversal rejection, and orphan revision cleanup. Prove crash/failure behavior with shared adapter contracts plus Android runtime and iOS Simulator tests. Keep UI, camera, OCR, PDF export, Foundry/source-aware artifacts, and dynamic behavioral-reference execution outside the slice.
