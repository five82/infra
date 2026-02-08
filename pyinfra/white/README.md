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
- Base packages (git, neovim, btop, mediainfo, etc.)
- Starship prompt, Atuin shell history, uv package manager
- Node.js via NVM
- NVIDIA headless driver and CUDA toolkit
- Go
- MakeMKV (Blu-ray/DVD ripper)
- Claude Code
