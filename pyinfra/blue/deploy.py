#!/usr/bin/env python3
"""Blue environment (Podman quadlets server) deployment.

Usage:
    pyinfra @local deploy.py --sudo
    pyinfra @local deploy.py --sudo --dry  # Dry run
"""

import os
import sys
from pathlib import Path

# Ensure we can import from this directory
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from operations import (
    tailscale,
    base_packages,
    podman_auto_update,
    nas_mount,
    nodejs,
    jellyfin,
    freshrss,
    caddy,
)

# Initialize configuration
config = Config()

# Determine target user (equivalent to SUDO_USER lookup)
target_user = os.environ.get("SUDO_USER") or os.environ.get("USER")
target_home = f"/home/{target_user}" if target_user else os.environ.get("HOME")

# Deploy operations in order
tailscale.deploy(config)
base_packages.deploy(config, target_user, target_home)
podman_auto_update.deploy(config)
nas_mount.deploy(config)
nodejs.deploy(config, target_user, target_home)
jellyfin.deploy(config, target_user, target_home)
freshrss.deploy(config, target_user, target_home)
caddy.deploy(config)
