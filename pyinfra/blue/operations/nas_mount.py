"""NAS NFS mount configuration."""

from pyinfra.operations import files, server


def deploy(config):
    """Configure NAS NFS mount."""

    # Ensure mount point exists
    files.directory(
        name="Ensure NAS mount point exists",
        path=config.nas_mount_point,
        mode="0755",
    )

    # Add NFS mount to fstab (mounted=False since noauto is in options)
    server.mount(
        name="Add NAS NFS mount for Jellyfin",
        path=config.nas_mount_point,
        device=f"{config.nas_mount_server}:{config.nas_mount_path}",
        fs_type="nfs4",
        options=config.nas_mount_opts.split(","),
        mounted=False,  # Don't mount now (noauto is in options)
    )
