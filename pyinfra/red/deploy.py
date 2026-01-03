#!/usr/bin/env python3
"""Red environment (NAS server) deployment.

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
    nodejs,
    storage,
    snapraid,
    nfs,
    samba,
)

# Initialize configuration
config = Config()

# Determine target user (equivalent to SUDO_USER lookup)
target_user = os.environ.get("SUDO_USER") or os.environ.get("USER")
target_home = f"/home/{target_user}" if target_user else os.environ.get("HOME")

# Deploy operations in order
tailscale.deploy(config)
base_packages.deploy(config, target_user, target_home)
nodejs.deploy(config, target_user, target_home)
storage.deploy(config)
snapraid.deploy(config)
nfs.deploy(config)
samba.deploy(config)
