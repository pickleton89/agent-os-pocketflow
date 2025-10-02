# Agent OS + PocketFlow v2 Migration Guide

This guide helps existing Agent OS + PocketFlow users move from the legacy
bash-based installers to the uv-packaged `agent-os` CLI introduced in the
2.0.0 release. Follow these steps if you previously cloned this repository
and ran `setup.sh`, `setup/base.sh`, or `setup/project.sh` manually.

## Who Should Use This Guide
- You currently rely on `~/agent-os-pocketflow` (or another clone) to install
  updates.
- Your base installation lives at `~/.agent-os/` and was last refreshed with
  the bash setup scripts.
- You have one or more projects that run `~/.agent-os/setup/project.sh` and
  want to keep them aligned with the new distribution channel.

## What Changed in 2.0.0
- **uv-native distribution**: Install and update the framework with
  `uv tool install agent-os-pocketflow` or `uv pip install -e .`.
- **`agent-os` CLI**: Replaces `setup.sh` as the entry point. Supports
  `agent-os init` with rich reporting, confirmation prompts, and force-safe
  overwrites.
- **Packaged resources**: Instructions, standards, framework tools, and
  templates ship inside the wheel so installs no longer depend on cloning the
  repository.
- **Backward-compatible scripts**: `setup/project.sh` and
  `setup/update-project.sh` still exist inside the installation, but the base
  payload now comes from the Python package.

## Quick Migration Checklist
1. Confirm prerequisites (`uv --version`, `python3 --version`, clean git status in the
   clone you are upgrading).
2. Back up the current base installation.
3. Install the new CLI (`uv tool install` or editable `uv pip install -e .`).
4. Run `agent-os init --force` to rebuild the base.
5. Update each project using `~/.agent-os/setup/update-project.sh --update-all`.
6. Validate the new toolchain and remove backups when satisfied.

## Step-by-Step Migration

### 1. Audit Your Current State
```bash
# Check uv and python
uv --version
python3 --version

# Optional: list uv-managed runtimes
# uv python list

# Confirm where your existing base install lives
ls ~/.agent-os
```
If your base directory already contains custom changes, note them so you can
re-apply after the upgrade.

### 2. Back Up the Legacy Base Installation
```bash
# Create a timestamped backup before overwriting anything
timestamp=$(date +%Y%m%d-%H%M%S)
cp -a ~/.agent-os ~/.agent-os-backup-$timestamp
```
Repeat for any project-local `.agent-os/` directories you plan to update.

### 3. Install the `agent-os` CLI via uv
Pick the option that matches your workflow:

```bash
# Install from GitHub (most users)
uv tool install --from "git+https://github.com/pickleton89/agent-os-pocketflow.git" agent-os-pocketflow

# OR: from a local clone while developing
uv tool install --from "$PWD" agent-os-pocketflow
# OR keep an editable install for hacking on the framework
uv pip install -e .
```
After installation, confirm the binary is on your PATH:
```bash
agent-os --version
```

### 4. Rebuild the Base Installation
```bash
agent-os init --force --yes
```
Commonly used flags:
- `--install-path PATH` to place the base somewhere other than `~/.agent-os`.
- `--no-pocketflow` or `--no-claude-code` to trim optional bundles.
- `--show-paths` for a verbose list of created/overwritten files.

The command prints a summary table of created and overwritten paths. Review it
before deleting your backup.

### 5. Update Project Installations
For every repository that depends on the base installation:
```bash
cd /path/to/project
~/.agent-os/setup/update-project.sh --update-all --force
```
If a project keeps its own `.agent-os/` copy under version control, rebuild it
in place instead:
```bash
uvx --from "git+https://github.com/pickleton89/agent-os-pocketflow.git" \
  agent-os init --install-path .agent-os --force --yes
```
Then rerun the project script if you skipped the base entirely:
```bash
./.agent-os/setup/project.sh --no-base --claude-code --force
```

### 6. Validate the Upgrade
```bash
agent-os init --show-paths --yes --no-force  # Dry-run confirmation prompt
~/.agent-os/setup/project.sh --help
~/.agent-os/setup/update-project.sh --help
uv run pytest -q framework-tools  # Optional: framework regression check
```
Spot-check a project workflow (e.g., `/execute-tasks`) to ensure the updated
instructions and templates behave as expected. Remove the backup directories
only after this validation step passes.

## Rollback Plan
If you encounter an issue you cannot resolve quickly:
1. Remove or rename the new installation (`rm -rf ~/.agent-os`).
2. Restore your backup (`mv ~/.agent-os-backup-<timestamp> ~/.agent-os`).
3. Revert to the previous installation method (clone + `setup.sh`).

Keep the `agent-os --version` output with any bug report so we can reproduce
and address migration issues.

## Legacy vs. New Commands
| Legacy Action | Legacy Command | New Workflow |
|---------------|----------------|--------------|
| Install base resources | `./setup.sh base` | `agent-os init [options]` |
| Force overwrite base | `./setup/base.sh --force` | `agent-os init --force --yes` |
| Install project assets | `./setup.sh project` | `~/.agent-os/setup/project.sh` |
| Update project assets | `./setup/update-project.sh` | `~/.agent-os/setup/update-project.sh --update-all` |
| Run installer without cloning | _Not supported_ | `uvx --from <source> agent-os init` |

## Troubleshooting
- **`agent-os` not found**: Re-run `uv tool install ...` and ensure the uv tool
  binary directory is exported in your shell (`uv tool list --show-path`).
- **Existing install detected**: Use `agent-os init --force --yes` after taking
  a backup. The CLI refuses to overwrite without `--force` to prevent data loss.
- **Custom toolkit path**: Pass `--toolkit-source /path/to/framework-tools` when
  you need to seed from a modified toolkit directory.
- **Network-restricted environments**: Build the wheel once (e.g., CI), host it
  internally, then reference that URL with `uv tool install --from`.

## Additional Resources
- `README.md` — Updated installation instructions and CLI reference.
- `docs/uv-implementation-plan.md` — Full rollout plan with validation steps.
- `CHANGELOG.md` — Release history leading up to 2.0.0.

Report any migration blockers through the issue tracker with details about
platform, uv version, and the exact command output.
