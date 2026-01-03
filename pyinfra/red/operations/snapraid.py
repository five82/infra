"""SnapRAID configuration."""

from pathlib import Path

from pyinfra.operations import apt, files, systemd


def deploy(config):
    """Deploy SnapRAID configuration."""

    templates_dir = Path(__file__).parent.parent / "templates"
    files_dir = Path(__file__).parent.parent / "files"

    # Install snapraid
    apt.packages(
        name="Install snapraid",
        packages=["snapraid"],
    )

    # Deploy config template
    files.template(
        name="Install snapraid configuration",
        src=str(templates_dir / "snapraid.conf.j2"),
        dest="/etc/snapraid.conf",
        user="root",
        group="root",
        mode="0644",
        snapraid_parity_path=config.snapraid_parity_path,
        snapraid_content_paths=config.snapraid_content_paths,
        snapraid_data_disks=config.snapraid_data_disks,
        snapraid_excludes=config.snapraid_excludes,
    )

    # Deploy systemd units
    units_changed = False
    for unit in config.snapraid_systemd_units:
        result = files.put(
            name=f"Install snapraid systemd unit: {unit}",
            src=str(files_dir / unit),
            dest=f"/etc/systemd/system/{unit}",
            user="root",
            group="root",
            mode="0644",
        )
        if result.changed:
            units_changed = True

    # Reload systemd if units changed
    if units_changed:
        systemd.daemon_reload(
            name="Reload systemd daemon",
        )

    # Enable and start timers
    for timer in config.snapraid_timers:
        systemd.service(
            name=f"Enable and start snapraid timer: {timer}",
            service=timer,
            enabled=True,
            running=True,
        )
