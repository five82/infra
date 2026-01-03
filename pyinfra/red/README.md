# Red Environment (NAS Server)

Pyinfra deployment for the red NAS server (Raspberry Pi 5).

## Prerequisites

Install pyinfra:

```bash
uv tool install pyinfra
```

## Setup

1. Create the secrets file:

```bash
cp secrets.example.py secrets.py
```

2. Edit `secrets.py` and set the Samba password:

```python
smb_password = "your-actual-password"
```

## Usage

Run from this directory:

```bash
# Dry run (preview changes)
pyinfra @local deploy.py --sudo --dry

# Apply changes
pyinfra @local deploy.py --sudo
```

## What it configures

- Tailscale VPN
- Base packages (git, neovim, btop, etc.)
- Starship prompt, Atuin shell history, uv package manager
- Node.js via NVM
- Storage (mergerfs pool, XFS disk mounts)
- SnapRAID (parity protection with sync/scrub timers)
- NFS server
- Samba shares
