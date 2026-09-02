# ChatGPT Web Operator Contract

AppFusion must remain usable when Codex and every local machine are offline.

## Session bootstrap and app selection

At the start of every new chat, the operator reads `environment-manifest.json`, then reconciles the GitHub mirror at `state/APPFUSION_PROJECT_REGISTRY.json` with Drive registry file `15-oC17tb-17N_5h6vKsYGct7_D_xGGqI` in `00_CONTROL`. Chat history and model memory are convenience context, never state authority.

The registry drives selection: no active app is reported as such, one active app is resumed automatically, and multiple active apps are listed for explicit user selection. The operator reports the system/app phase, last completed event, blockers, and next safe action before continuing. The portable first-message prompt is in `NEW_CHAT_BOOTSTRAP.md`.

## Interactive-resumable operation

From ChatGPT web, an authenticated user may use the installed Google Drive and GitHub plugins to:

1. place authorized APK inputs in the private Drive intake folder;
2. obtain the Drive file identity and SHA-256 evidence;
3. create an `IntakeRequest` under `requests/pending/` through GitHub;
4. trigger or monitor the registration workflow;
5. inspect Foundry reports and the clean-room `ProductBlueprint`;
6. explicitly approve the exact Product Blueprint hash;
7. monitor Product Foundry build/test/release evidence.

All commands are versioned data contracts. The web chat is a control surface, not the state database.

Every material transition appends a `RunEvent` and updates the Drive copy of the affected `ApplicationState` and project registry. The GitHub mirror is updated only at a code change, exact-hash approval, milestone, or release boundary.

If the reasoning session ends, completed deterministic CI work and all committed/event artifacts remain resumable. A later ChatGPT web or Codex session reads the same state and continues.

## Unattended operation

Closing ChatGPT web ends interactive model reasoning. True unattended reasoning therefore requires the persistent coordinator described by `SYSTEM_V1_UA`, deployed outside the chat session with:

- an authorized OpenAI API project/service identity;
- a durable queue and leases;
- GitHub App or narrowly scoped repository credentials;
- Google workload identity or approved storage credentials;
- explicit metered-model budget limits;
- approval/deviation enforcement.

Until those credentials and budgets are configured, AppFusion reports `INTERACTIVE_RESUMABLE`, not unattended autonomy.

## GitHub budget discipline

ChatGPT performs reasoning, synthesis, comparison, and report drafting. Drive stores high-frequency working state, source inputs, reports, screenshots, videos, and other bulky artifacts. GitHub stores version-controlled source, policies, schemas, small checkpoint manifests, and releases; GitHub Actions runs only reproducible builds, tests, security gates, or release work that materially benefits from CI. Ordinary reasoning, document review, idle polling, and bulky artifact storage must not consume Actions minutes.

## No local dependency

The optional local CLI may validate the same schemas or assist debugging. It cannot become canonical, contain the only copy of an artifact, or be required by a GitHub workflow. Local paths must never appear in committed requests or policy.
