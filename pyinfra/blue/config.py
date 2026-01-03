"""Blue environment configuration defaults."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    # Tailscale
    tailscale_distro: str = "raspbian"
    tailscale_release: str = "trixie"

    # Base packages
    timezone: str = "America/New_York"
    apt_packages: List[str] = field(default_factory=lambda: [
        "git",
        "gh",
        "neovim",
        "curl",
        "bash-completion",
        "ripgrep",
        "btop",
        "podman",
        "unattended-upgrades",
        "nfs-common",
    ])

    # Node.js
    nvm_version: str = "v0.40.3"
    nodejs_version: str = "25"

    # Podman auto-update
    podman_auto_update_timer: str = "podman-auto-update.timer"

    # NAS mount
    nas_mount_server: str = "10.100.90.3"
    nas_mount_path: str = "/"
    nas_mount_point: str = "/media/daspool"
    nas_mount_opts: str = "noauto,x-systemd.automount,_netdev,nofail,hard,timeo=600,retrans=2"

    # Jellyfin
    jellyfin_image: str = "docker.io/jellyfin/jellyfin:latest"
    jellyfin_http_port: int = 8096
    jellyfin_autodiscovery_port: int = 7359
    jellyfin_dlna_port: int = 1900
    jellyfin_devices: List[str] = field(default_factory=lambda: [
        "/dev/video19",
        "/dev/dri/renderD128",
    ])
    jellyfin_media_path: str = "/media/daspool/media"

    # FreshRSS
    freshrss_image: str = "lscr.io/linuxserver/freshrss:latest"
    freshrss_port: int = 20009
    freshrss_timezone: str = "Etc/UTC"

    # Caddy
    caddy_image: str = "ghcr.io/caddybuilds/caddy-cloudflare:latest"
    caddy_jellyfin_domain: str = "jellyfin.home.five82.xyz"
    caddy_jellyfin_upstream: str = "127.0.0.1:8096"
