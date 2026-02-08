"""Jellyfin container quadlet configuration."""

import os
from pathlib import Path

from pyinfra import host
from pyinfra.operations import files, server, systemd
from pyinfra.facts.server import Command


def deploy(config, target_user, target_home):
    """Deploy Jellyfin quadlet."""

    templates_dir = Path(__file__).parent.parent / "templates"

    # Fail if running as root without SUDO_USER
    if not os.environ.get("SUDO_USER") and os.environ.get("USER") == "root":
        raise RuntimeError(
            "Refusing to manage Jellyfin config under HOME without SUDO_USER"
        )

    # Get user info
    getent = host.get_fact(Command, f"getent passwd {target_user}")
    parts = getent.split(":")
    user_home = parts[5]
    user_uid = parts[2]
    user_gid = parts[3]

    # Add user to video group
    server.user(
        name="Ensure Jellyfin user is in video group",
        user=target_user,
        groups=["video"],
    )

    # Create config/cache directories (use username, not UID, for idempotency)
    for subdir in ["", "/config", "/cache"]:
        files.directory(
            name=f"Ensure Jellyfin directory exists: {user_home}/.jellyfin{subdir}",
            path=f"{user_home}/.jellyfin{subdir}",
            user=target_user,
            group=target_user,
            mode="0755",
        )

    # Ensure quadlet directory exists
    files.directory(
        name="Ensure quadlet directory exists",
        path="/etc/containers/systemd",
        user="root",
        group="root",
        mode="0755",
    )

    # Deploy quadlet template
    quadlet_result = files.template(
        name="Install Jellyfin quadlet",
        src=str(templates_dir / "jellyfin.container.j2"),
        dest="/etc/containers/systemd/jellyfin.container",
        user="root",
        group="root",
        mode="0644",
        jellyfin_image=config.jellyfin_image,
        jellyfin_uid=user_uid,
        jellyfin_gid=user_gid,
        jellyfin_http_port=config.jellyfin_http_port,
        jellyfin_autodiscovery_port=config.jellyfin_autodiscovery_port,
        jellyfin_dlna_port=config.jellyfin_dlna_port,
        jellyfin_devices=config.jellyfin_devices,
        jellyfin_config_dir=f"{user_home}/.jellyfin/config",
        jellyfin_cache_dir=f"{user_home}/.jellyfin/cache",
        jellyfin_media_path=config.jellyfin_media_path,
    )

    # Reload systemd if quadlet changed
    if quadlet_result.changed:
        systemd.daemon_reload(
            name="Reload systemd daemon",
        )

    # Start Jellyfin (boot enablement handled by [Install] section in quadlet file)
    systemd.service(
        name="Start Jellyfin",
        service="jellyfin.service",
        running=True,
        restarted=quadlet_result.changed,
    )
