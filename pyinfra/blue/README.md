# Blue Environment (Podman Quadlets Server)

Pyinfra deployment for the blue server (Raspberry Pi 5) running containerized services.

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

2. Edit `secrets.py` and set the Cloudflare API token:

```python
caddy_cloudflare_api_token = "your-actual-token"
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
- Base packages (git, neovim, btop, podman, etc.)
- Starship prompt, Atuin shell history, uv package manager
- Node.js via NVM
- Podman auto-update timer
- NAS NFS mount (`/media/daspool`)
- Jellyfin (media server container)
- FreshRSS (RSS reader container)
- Caddy (reverse proxy with Cloudflare DNS-01 HTTPS)
