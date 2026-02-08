"""Tailscale VPN client installation."""

from pyinfra.operations import apt, files, systemd


def deploy(config):
    """Deploy Tailscale VPN client."""

    # Ensure keyring directory exists
    files.directory(
        name="Ensure Tailscale keyring directory exists",
        path="/usr/share/keyrings",
        mode="0755",
    )

    # Download GPG key
    gpg_url = f"https://pkgs.tailscale.com/stable/{config.tailscale_distro}/{config.tailscale_release}.noarmor.gpg"
    key_result = files.download(
        name="Install Tailscale repository key",
        src=gpg_url,
        dest="/usr/share/keyrings/tailscale-archive-keyring.gpg",
        mode="0644",
    )

    # Download repo list
    list_url = f"https://pkgs.tailscale.com/stable/{config.tailscale_distro}/{config.tailscale_release}.tailscale-keyring.list"
    list_result = files.download(
        name="Install Tailscale repository list",
        src=list_url,
        dest="/etc/apt/sources.list.d/tailscale.list",
        mode="0644",
    )

    # Update apt cache if repo changed
    if key_result.changed or list_result.changed:
        apt.update(
            name="Update apt cache after adding Tailscale repo",
        )

    # Install tailscale
    apt.packages(
        name="Install Tailscale",
        packages=["tailscale"],
    )

    # Enable and start service
    systemd.service(
        name="Ensure Tailscale daemon is enabled and started",
        service="tailscaled",
        enabled=True,
        running=True,
    )
