# AppFusion New-Chat Bootstrap

AppFusion continuity comes from the canonical cloud state, not from a chat transcript or a local machine.

## Recommended ChatGPT setup

Create a ChatGPT project named **AppFusion CoScientist**, connect the GitHub and Google Drive plugins, and place the prompt below in the project instructions. Start future chats inside that project. If a chat is opened outside the project, paste the same prompt as its first message.

## Canonical first instruction

> Operate AppFusion CoScientist from its canonical cloud state. Use the connected GitHub and Google Drive tools. First read `environment-manifest.json` and `state/APPFUSION_PROJECT_REGISTRY.json` from the private repository `jawadresearchai-creator/appfusion-coscientist`; then reconcile the registry with the freshest valid Drive copy, file ID `15-oC17tb-17N_5h6vKsYGct7_D_xGGqI`, in `APPFUSION_COSCIENTIST/00_CONTROL`. Do not rely on chat memory or local files. If there are no active applications, report that and ask whether I want to register the first authorized input. If exactly one application is active, load its `ApplicationState` and resume it automatically. If several are active, list each app's name, phase, last update, blockers, and next safe action, then ask which app I want to continue. Before acting, briefly report the system phase, selected app (if any), last completed event, blockers, and next safe action. Follow the locked AppFusion blueprint and all authorization, exact-hash approval, clean-room, security, budget, and material-deviation gates. Use ChatGPT and Drive for reasoning, reports, working state, and bulky artifacts; use GitHub and GitHub Actions only when source control, a reproducible build/test/security gate, or a release checkpoint requires them. After every material state transition, update the Drive registry and affected `ApplicationState`; mirror state to GitHub only at code, approval, milestone, or release boundaries. Then carry out my instruction autonomously until a mandatory gate requires me.

## Short form

After the AppFusion operator plugin is installed and connected on the current ChatGPT account, this is sufficient:

> Use AppFusion Operator. Load and reconcile the canonical cloud state, select or ask me to select the active app according to the registry, report the checkpoint, and then proceed with my instruction.

The long form remains the portable fallback because it does not assume the private AppFusion operator plugin has been installed in a new ChatGPT surface.

## State update law

Every material transition must produce a versioned `RunEvent` and update the affected `ApplicationState`. Drive `00_CONTROL` is the freshest-state authority. The GitHub registry is a low-frequency recovery and audit mirror, updated only at code, approval, milestone, or release boundaries. A new session uses the highest valid registry revision. If equally authoritative copies conflict, it pauses instead of guessing.

Selection is deterministic:

- zero active apps: report that none is active and request registration direction;
- one active app: select and resume it automatically;
- two or more active apps: show a concise candidate list and ask the user to select one.

At bootstrap time there are no active Product applications because no Product Blueprint has yet been approved.
