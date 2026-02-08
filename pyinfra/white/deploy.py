#!/usr/bin/env python3
"""White environment (Debian Trixie amd64) deployment.

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
from operations import tailscale, base_packages, nvidia, golang, nodejs, makemkv, claude_code

# Initialize configuration
config = Config()

# Determine target user (equivalent to SUDO_USER lookup)
target_user = os.environ.get("SUDO_USER") or os.environ.get("USER")
target_home = f"/home/{target_user}" if target_user else os.environ.get("HOME")

# Deploy operations in order
tailscale.deploy(config)
base_packages.deploy(config, target_user, target_home)
nvidia.deploy(config)
golang.deploy(config)
nodejs.deploy(config, target_user, target_home)
makemkv.deploy(config)
claude_code.deploy(config, target_user, target_home)
