"""Podman auto-update timer configuration."""

from pyinfra.operations import systemd


def deploy(config):
    """Enable Podman auto-update timer."""

    systemd.service(
        name="Enable Podman auto-update timer",
        service=config.podman_auto_update_timer,
        enabled=True,
        running=True,
    )
