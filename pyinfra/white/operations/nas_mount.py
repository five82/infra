"""NAS NFS mount configuration."""

from pyinfra.operations import files, systemd


def deploy(config):
    """Configure NAS NFS mount."""

    # Ensure mount point exists
    files.directory(
        name="Ensure NAS mount point exists",
        path=config.nas_mount_point,
        mode="0755",
    )

    # Add NFS mount to fstab
    fstab_line = (
        f"{config.nas_mount_server}:{config.nas_mount_path} "
        f"{config.nas_mount_point} nfs4 "
        f"{config.nas_mount_opts} 0 0"
    )
    fstab_updated = files.line(
        name="Add NAS NFS mount to fstab",
        path="/etc/fstab",
        line=fstab_line,
    )

    # Reload systemd to pick up the new automount unit
    systemd.daemon_reload(
        name="Reload systemd after fstab change",
        _if=lambda: fstab_updated.changed,
    )

    # Ensure the automount unit is started
    mount_unit = config.nas_mount_point.strip("/").replace("/", "-")
    systemd.service(
        name="Ensure NAS automount is started",
        service=f"{mount_unit}.automount",
        running=True,
        enabled=False,  # Generated from fstab, cannot be enabled explicitly
    )
