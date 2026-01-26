"""FreshRSS container quadlet configuration."""

import os
from pathlib import Path

from pyinfra import host
from pyinfra.operations import files, systemd
from pyinfra.facts.server import Command


def deploy(config, target_user, target_home):
    """Deploy FreshRSS quadlet."""

    templates_dir = Path(__file__).parent.parent / "templates"

    # Fail if running as root without SUDO_USER
    if not os.environ.get("SUDO_USER") and os.environ.get("USER") == "root":
        raise RuntimeError(
            "Refusing to manage FreshRSS config under HOME without SUDO_USER"
        )

    # Get user info
    getent = host.get_fact(Command, f"getent passwd {target_user}")
    parts = getent.split(":")
    user_uid = parts[2]
    user_gid = parts[3]

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
        name="Install FreshRSS quadlet",
        src=str(templates_dir / "freshrss.container.j2"),
        dest="/etc/containers/systemd/freshrss.container",
        user="root",
        group="root",
        mode="0644",
        freshrss_image=config.freshrss_image,
        freshrss_uid=user_uid,
        freshrss_gid=user_gid,
        freshrss_timezone=config.freshrss_timezone,
        freshrss_port=config.freshrss_port,
    )

    # Reload systemd if quadlet changed
    if quadlet_result.changed:
        systemd.daemon_reload(
            name="Reload systemd daemon",
        )

    # Start FreshRSS (boot enablement handled by [Install] section in quadlet file)
    systemd.service(
        name="Start FreshRSS",
        service="freshrss.service",
        running=True,
        restarted=quadlet_result.changed,
    )
