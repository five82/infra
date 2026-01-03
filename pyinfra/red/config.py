"""Red environment configuration defaults."""

from dataclasses import dataclass, field
from typing import List, Dict


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
        "tree",
        "unattended-upgrades",
    ])

    # Node.js
    nvm_version: str = "v0.40.3"
    nodejs_version: str = "25"

    # Storage
    storage_packages: List[str] = field(default_factory=lambda: [
        "mergerfs",
        "fuse3",
    ])
    data_disks: List[Dict[str, str]] = field(default_factory=lambda: [
        {"path": "/mnt/das1", "label": "das1"},
        {"path": "/mnt/das2", "label": "das2"},
        {"path": "/mnt/das3", "label": "das3"},
    ])
    parity_disk: Dict[str, str] = field(default_factory=lambda: {
        "path": "/mnt/parity1",
        "label": "parity1",
    })
    pool_path: str = "/media/daspool"
    pool_sources: str = "/mnt/das1:/mnt/das2:/mnt/das3"
    pool_opts: str = "defaults,allow_other,use_ino,category.create=mfs,moveonenospc=true"

    # Snapraid
    snapraid_parity_path: str = "/mnt/parity1/snapraid.parity"
    snapraid_content_paths: List[str] = field(default_factory=lambda: [
        "/mnt/das1/snapraid.content",
        "/mnt/das2/snapraid.content",
        "/mnt/das3/snapraid.content",
        "/mnt/parity1/snapraid.content",
    ])
    snapraid_data_disks: List[Dict[str, str]] = field(default_factory=lambda: [
        {"name": "d1", "path": "/mnt/das1"},
        {"name": "d2", "path": "/mnt/das2"},
        {"name": "d3", "path": "/mnt/das3"},
    ])
    snapraid_excludes: List[str] = field(default_factory=lambda: [
        "/lost+found/",
    ])
    snapraid_systemd_units: List[str] = field(default_factory=lambda: [
        "snapraid-sync.service",
        "snapraid-sync.timer",
        "snapraid-scrub.service",
        "snapraid-scrub.timer",
    ])
    snapraid_timers: List[str] = field(default_factory=lambda: [
        "snapraid-sync.timer",
        "snapraid-scrub.timer",
    ])

    # NFS
    nfs_exports: List[Dict[str, str]] = field(default_factory=lambda: [
        {
            "path": "/media/daspool",
            "clients": "10.100.90.0/24",
            "options": "rw,async,no_subtree_check,fsid=0",
        },
    ])

    # Samba
    samba_shares: List[Dict[str, str]] = field(default_factory=lambda: [
        {
            "name": "daspool",
            "path": "/media/daspool",
            "browseable": "yes",
            "read_only": "no",
            "guest_ok": "no",
            "valid_users": "ken",
            "force_user": "ken",
            "create_mask": "0664",
            "directory_mask": "0775",
        },
    ])
    samba_user: str = "ken"
