"""Storage configuration - mergerfs and disk mounts."""

from pyinfra.operations import apt, files, server


def deploy(config):
    """Deploy storage configuration."""

    # Install storage packages
    apt.packages(
        name="Install storage packages",
        packages=config.storage_packages,
    )

    # Create data disk mount points
    for disk in config.data_disks:
        files.directory(
            name=f"Ensure data disk mount point exists: {disk['path']}",
            path=disk["path"],
            mode="0755",
        )

    # Create parity disk mount point
    files.directory(
        name="Ensure parity disk mount point exists",
        path=config.parity_disk["path"],
        mode="0755",
    )

    # Create pool mount point
    files.directory(
        name="Ensure pool mount point exists",
        path=config.pool_path,
        mode="0755",
    )

    # Mount data disks
    for disk in config.data_disks:
        server.mount(
            name=f"Mount data disk: {disk['label']}",
            path=disk["path"],
            device=f"LABEL={disk['label']}",
            fs_type="xfs",
            options=["defaults"],
            mounted=True,
        )

    # Mount parity disk
    server.mount(
        name="Mount parity disk",
        path=config.parity_disk["path"],
        device=f"LABEL={config.parity_disk['label']}",
        fstype="xfs",
        options=["defaults"],
        mounted=True,
        permanent=True,
    )

    # Configure FUSE allow_other
    files.line(
        name="Allow FUSE allow_other",
        path="/etc/fuse.conf",
        line="user_allow_other",
        replace="^#?user_allow_other.*",
    )

    # Mount mergerfs pool
    server.mount(
        name="Mount mergerfs pool",
        path=config.pool_path,
        device=config.pool_sources,
        fs_type="fuse.mergerfs",
        options=config.pool_opts.split(","),
        mounted=True,
        permanent=True,
    )
