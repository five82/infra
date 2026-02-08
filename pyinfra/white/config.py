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
        "mediainfo",
        "mkvtoolnix",
        "build-essential",
        "cmake",
        "nasm",
        "yasm",
        "pkg-config",
        "wget",
        "autoconf",
        "automake",
        "libtool",
        "clang",
        "libva-dev",
        "libva-drm2",
        "libva-x11-2",
        "libva2",
        "meson",
        "ninja-build",
        "zsh-autosuggestions",
        "zsh-syntax-highlighting",
        "bat",
        "lsd",
        "fd-find",
    ])

    # NVIDIA
    nvidia_cuda_repo_distro: str = "debian13"
    nvidia_cuda_keyring_url: str = "https://developer.download.nvidia.com/compute/cuda/repos/debian13/x86_64/cuda-keyring_1.1-1_all.deb"
    nvidia_driver_packages: List[str] = field(default_factory=lambda: [
        "nvidia-driver-cuda",
        "nvidia-kernel-open-dkms",
    ])
    nvidia_cuda_packages: List[str] = field(default_factory=lambda: [
        "cuda-toolkit",
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
