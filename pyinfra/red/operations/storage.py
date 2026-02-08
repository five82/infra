"""Storage configuration - mergerfs and disk mounts."""

from pyinfra import host
from pyinfra.operations import apt, files, server
from pyinfra.facts.server import Mounts


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

    # Get current mounts for idempotency checks
    current_mounts = host.get_fact(Mounts)

    # Mount data disks (fstab + mount if not mounted)
    for disk in config.data_disks:
        fstab_entry = f"LABEL={disk['label']} {disk['path']} xfs defaults 0 0"
        files.line(
            name=f"Add data disk to fstab: {disk['label']}",
            path="/etc/fstab",
            line=fstab_entry,
        )
        if disk["path"] not in current_mounts:
            server.shell(
                name=f"Mount data disk: {disk['label']}",
                commands=[f"mount {disk['path']}"],
            )

    # Mount parity disk (fstab + mount if not mounted)
    parity_fstab = f"LABEL={config.parity_disk['label']} {config.parity_disk['path']} xfs defaults 0 0"
    files.line(
        name="Add parity disk to fstab",
        path="/etc/fstab",
        line=parity_fstab,
    )
    if config.parity_disk["path"] not in current_mounts:
        server.shell(
            name="Mount parity disk",
            commands=[f"mount {config.parity_disk['path']}"],
        )

    # Configure FUSE allow_other
    files.line(
        name="Allow FUSE allow_other",
        path="/etc/fuse.conf",
        line="user_allow_other",
        replace="^#?user_allow_other.*",
    )

    # Add mergerfs pool to fstab directly (server.mount doesn't handle FUSE well)
    fstab_line = f"{config.pool_sources} {config.pool_path} fuse.mergerfs {config.pool_opts} 0 0"
    files.line(
        name="Add mergerfs pool to fstab",
        path="/etc/fstab",
        line=fstab_line,
    )

    # Mount mergerfs pool if not already mounted
    if config.pool_path not in current_mounts:
        server.shell(
            name="Mount mergerfs pool",
            commands=[f"mount {config.pool_path}"],
        )
