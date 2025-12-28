# AGENTS.md

## Project overview
- **red**: NAS server.
- **blue**: Podman quadlets server running Jellyfin and other containers.
- Both are Raspberry Pi 5 boxes running Raspberry Pi OS Trixie.

## Repo layout
- `red/`: NAS server configuration and playbooks.
- `blue/`: Podman quadlets server configuration and playbooks.

## Conventions
- Prefer minimal, clear changes.
- Keep environment-specific differences confined to their respective directories.
- When adding packages, update the base packages role for the target environment.
- Prefer proper role separation; avoid piling unrelated concerns into base_packages.
- Avoid changing storage, mount, or filesystem settings on **red** unless explicitly requested.
- Avoid altering quadlet definitions or container volumes on **blue** unless explicitly requested.
- Containers should use Podman named volumes and include the auto-update label.

## Ansible
- Playbooks live under each environment's `playbooks/`.
- Roles live under each environment's `roles/`.
- Entry points are the playbooks under each environment's `playbooks/` directory.

## Secrets
- Do not create, modify, or move secrets unless explicitly requested.
- If a change needs credentials, ask where the secret should live before proceeding.

## Validation
- Prefer `ansible-playbook --check` for dry runs when unsure.
- Call out any expected service restarts or downtime.
- When adding or updating quadlets, ensure systemd daemon reload happens before enabling/starting the generated service.

## Operational constraints
- Assume headless operation.
- Do not reboot or restart critical services unless explicitly requested.

## Notes
- Jellyfin runs on **blue** via Podman quadlets.
