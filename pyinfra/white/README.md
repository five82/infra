# White Environment (Desktop Workstation)

Pyinfra deployment for the white workstation (Debian Trixie amd64).

## Prerequisites

Install pyinfra:

```bash
uv tool install pyinfra
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
- Base packages (git, neovim, ripgrep, btop, bat, lsd, fd-find, mediainfo, etc.)
- Starship prompt, Atuin shell history, uv package manager
- NAS NFS automount (10.100.90.3:/ → /media/daspool)
- Node.js via NVM
- NVIDIA headless driver and CUDA toolkit
- Go
- MakeMKV (Blu-ray/DVD ripper)
- Claude Code
