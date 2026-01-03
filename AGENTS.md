# AGENTS.md

## Project overview
- **red**: NAS server.
- **blue**: Podman quadlets server running Jellyfin and other containers.
- Both are Raspberry Pi 5 boxes running Raspberry Pi OS Trixie.

## Repo layout
- `pyinfra/red/`: NAS server configuration (primary).
- `pyinfra/blue/`: Podman quadlets server configuration (primary).
- `red/`: Legacy Ansible playbooks (reference only).
- `blue/`: Legacy Ansible playbooks (reference only).

## Conventions
- Prefer minimal, clear changes.
- Keep environment-specific differences confined to their respective directories.
- When adding packages, update the base packages operation for the target environment.
- Prefer proper operation separation; avoid piling unrelated concerns into base_packages.
- Avoid changing storage, mount, or filesystem settings on **red** unless explicitly requested.
- Avoid altering quadlet definitions or container volumes on **blue** unless explicitly requested.
- Containers should use Podman named volumes and include the auto-update label.

## Pyinfra
- Entry points are `pyinfra/red/deploy.py` and `pyinfra/blue/deploy.py`.
- Operations (equivalent to Ansible roles) live under `operations/`.
- Configuration defaults live in `config.py`.
- Templates use Jinja2 format in `templates/`.
- Static files live in `files/`.

## Secrets
- Secrets are stored in `secrets.py` (gitignored) with `secrets.example.py` as template.
- Do not create, modify, or move secrets unless explicitly requested.
- If a change needs credentials, ask where the secret should live before proceeding.

## Validation
- Use `pyinfra @local deploy.py --sudo --dry` for dry runs.
- Call out any expected service restarts or downtime.
- When adding or updating quadlets, ensure systemd daemon reload happens before starting the service.
- Quadlet services cannot be "enabled" (they're generator-managed); only start them.

## Operational constraints
- Assume headless operation.
- Do not reboot or restart critical services unless explicitly requested.

## Notes
- Jellyfin runs on **blue** via Podman quadlets.

## Legacy Ansible (reference only)
- Ansible playbooks in `red/` and `blue/` are kept for reference.
- New changes should be made to pyinfra, not Ansible.
- Ansible secrets used `vault.yml` (encrypted); pyinfra uses `secrets.py` (gitignored).
