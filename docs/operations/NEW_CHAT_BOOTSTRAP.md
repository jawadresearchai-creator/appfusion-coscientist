# AppFusion New-Chat Bootstrap

AppFusion continuity comes from the canonical cloud state, not from a chat transcript or a local machine.

**Mandatory cost rule:** no billing, paid service, paid trial, top-up or overage.
Read `docs/operations/FREE_ONLY_EXECUTION.md` before any executor dispatch. Monthly
free tiers are not the permanent solution. Do not request payment to resume.
Drive is storage, not compute. Public Product source was explicitly approved on
2026-09-04: `jawadresearchai-creator/appfusion-product-public` is the active Product
repository. Read `PUBLIC_PRODUCT_EXECUTION.md`. Keep Foundry, the historical
private Product repository, Drive and raw inputs private. Do not request this
same publication approval again or re-enable private workflows.

## Recommended ChatGPT setup

Create a ChatGPT project named **AppFusion CoScientist**, connect the GitHub and Google Drive plugins, and place the prompt below in the project instructions. Start future chats inside that project. If a chat is opened outside the project, paste the same prompt as its first message.

## Canonical first instruction

> Operate AppFusion CoScientist from its canonical cloud state. Use the connected GitHub and Google Drive tools. First read `environment-manifest.json`, `state/APPFUSION_PROJECT_REGISTRY.json`, the selected app's `state/applications/<app-id>.json`, its `state/delivery-plans/<plan-id>.json`, and the event tail from the private repository `jawadresearchai-creator/appfusion-coscientist`. Treat the committed Git event ledger as authoritative small control state. Read Drive control file `15-oC17tb-17N_5h6vKsYGct7_D_xGGqI` in `APPFUSION_COSCIENTIST/00_CONTROL` as a projection and bulky-artifact index; never let an older Drive projection overwrite a newer committed Git revision. Do not rely on chat memory or local files. If there are no active applications, report that and ask whether I want to register the first authorized input. If exactly one application is active, resume it automatically. If several are active, list each app's name, phase, last update, blockers, and next safe action, then ask which app I want to continue. Before acting, briefly report the phase, selected app, release-plan progress, last completed event, blockers, and next safe action. Follow the locked AppFusion blueprint, Delivery Orchestration v1.1, and all authorization, exact-hash approval, clean-room, security, budget, material-deviation, loop-limit, and release-readiness gates. Use ChatGPT and Drive for reasoning, reports, and bulky artifacts; use GitHub and GitHub Actions for source, atomic control-state transitions, reproducible build/test/security gates, and releases. Commit each material transition as one validated fast-forward state/event change, then project it to Drive. If the push is rejected or the expected revision changed, reload and pause or re-plan instead of overwriting. Continue autonomously until a mandatory gate requires me.

## Short form

After the AppFusion operator plugin is installed and connected on the current ChatGPT account, this is sufficient:

> Use AppFusion Operator. Load and reconcile the canonical cloud state, select or ask me to select the active app according to the registry, report the checkpoint, and then proceed with my instruction.

The long form remains the portable fallback because it does not assume the private AppFusion operator plugin has been installed in a new ChatGPT surface.

## State update law

Every material transition must produce one versioned `RunEvent`, update the affected `ApplicationState` and registry projection, validate the delivery plan, and land as an atomic fast-forward Git commit. Drive `00_CONTROL` is updated afterward as a human-readable projection and artifact index. A rejected push or mismatched expected revision is a conflict, not an invitation to choose the highest document and overwrite it.

Selection is deterministic:

- zero active apps: report that none is active and request registration direction;
- one active app: select and resume it automatically;
- two or more active apps: show a concise candidate list and ask the user to select one.

The registry currently contains one application active for selection, `docvault-lasttime-fusion`, so a new session should select it automatically. Active for selection does not mean execution is unblocked. At revision 20, its approved Product Blueprint and delivery plan `docvault-lasttime-fusion-v0.1` are preserved, Android J1 has passed, and execution is paused at the iOS executor boundary. Always read the current committed state for the latest phase and blockers instead of treating this explanatory example as live state.
