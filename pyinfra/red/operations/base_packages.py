"""Base packages and system configuration."""

import os
from pathlib import Path

from pyinfra import host
from pyinfra.operations import apt, files, server
from pyinfra.facts.server import Command
from pyinfra.facts.files import File


def deploy(config, target_user, target_home):
    """Deploy base packages and configuration."""

    # Fail if running as root without SUDO_USER
    if target_user == "root" and not os.environ.get("SUDO_USER"):
        raise RuntimeError(
            "Refusing to manage .bashrc without SUDO_USER; run via sudo as the target user."
        )

    files_dir = Path(__file__).parent.parent / "files"

    # Update apt cache
    apt.update(
        name="Update apt cache",
        cache_time=3600,
    )

    # Install base packages
    apt.packages(
        name="Install base packages",
        packages=config.apt_packages,
    )

    # Configure unattended upgrades
    files.put(
        name="Configure unattended upgrades (20auto-upgrades)",
        src=str(files_dir / "20auto-upgrades"),
        dest="/etc/apt/apt.conf.d/20auto-upgrades",
        user="root",
        group="root",
        mode="0644",
    )

    files.put(
        name="Configure unattended upgrades (50unattended-upgrades)",
        src=str(files_dir / "50unattended-upgrades"),
        dest="/etc/apt/apt.conf.d/50unattended-upgrades",
        user="root",
        group="root",
        mode="0644",
    )

    # Download and install Starship
    files.download(
        name="Download Starship installer",
        src="https://starship.rs/install.sh",
        dest="/tmp/starship-install.sh",
        mode="0755",
    )

    # Check if Starship is already installed
    starship_installed = host.get_fact(File, "/usr/local/bin/starship")
    if not starship_installed:
        server.shell(
            name="Install Starship",
            commands=["/tmp/starship-install.sh -y"],
        )

    # Download Atuin installer (no sudo)
    files.download(
        name="Download Atuin installer",
        src="https://setup.atuin.sh",
        dest="/tmp/atuin-install.sh",
        mode="0755",
        _sudo=False,
    )

    # Install Atuin (user-local, no sudo)
    atuin_bin = f"{target_home}/.atuin/bin/atuin"
    atuin_installed = host.get_fact(File, atuin_bin)
    if not atuin_installed:
        server.shell(
            name="Install Atuin",
            commands=["/bin/sh /tmp/atuin-install.sh"],
            _env={
                "HOME": target_home,
                "USER": target_user,
                "LOGNAME": target_user,
                "ATUIN_INSTALL_DIR": f"{target_home}/.atuin/bin",
            },
            _sudo=False,
        )

    # Download uv installer (no sudo)
    files.download(
        name="Download uv installer",
        src="https://astral.sh/uv/install.sh",
        dest="/tmp/uv-install.sh",
        mode="0755",
        _sudo=False,
    )

    # Install uv (user-local, no sudo)
    uv_bin = f"{target_home}/.local/bin/uv"
    uv_installed = host.get_fact(File, uv_bin)
    if not uv_installed:
        server.shell(
            name="Install uv",
            commands=["/bin/sh /tmp/uv-install.sh"],
            _env={
                "HOME": target_home,
                "USER": target_user,
            },
            _sudo=False,
        )

    # Manage user .bashrc
    files.put(
        name="Manage user .bashrc",
        src=str(files_dir / "bashrc"),
        dest=f"{target_home}/.bashrc",
        user=target_user,
        group=target_user,
        mode="0644",
        _sudo=False,
    )

    # Set timezone
    current_tz = host.get_fact(Command, "timedatectl show -p Timezone --value")
    if current_tz != config.timezone:
        server.shell(
            name="Set system timezone",
            commands=[f"timedatectl set-timezone {config.timezone}"],
        )
