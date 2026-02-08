"""White environment configuration defaults."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    # Tailscale
    tailscale_distro: str = "debian"
    tailscale_release: str = "trixie"

    # Base packages
    timezone: str = "America/New_York"
    apt_packages: List[str] = field(default_factory=lambda: [
        "zsh",
        "neovim",
        "git",
        "gh",
        "curl",
        "ripgrep",
        "btop",
        "tree",
        "unattended-upgrades",
    ])

    # Go
    go_version: str = "1.25.7"

    # MakeMKV
    makemkv_version: str = "1.18.3"
    makemkv_build_deps: List[str] = field(default_factory=lambda: [
        "build-essential",
        "pkg-config",
        "libc6-dev",
        "libssl-dev",
        "libexpat1-dev",
        "libavcodec-dev",
        "zlib1g-dev",
    ])

    # Node.js
    nvm_version: str = "v0.40.2"
    nodejs_version: str = "25"
