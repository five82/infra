"""NFS server configuration."""

from pathlib import Path

from pyinfra.operations import apt, files, server, systemd


def deploy(config):
    """Deploy NFS server configuration."""

    templates_dir = Path(__file__).parent.parent / "templates"

    # Install NFS server
    apt.packages(
        name="Install NFS server",
        packages=["nfs-kernel-server"],
    )

    # Ensure exports.d directory exists
    files.directory(
        name="Ensure NFS exports.d directory exists",
        path="/etc/exports.d",
        mode="0755",
    )

    # Deploy exports template
    exports_result = files.template(
        name="Install NFS export for daspool",
        src=str(templates_dir / "daspool.exports.j2"),
        dest="/etc/exports.d/daspool.exports",
        user="root",
        group="root",
        mode="0644",
        nfs_exports=config.nfs_exports,
    )

    # Reload exports if changed
    if exports_result.changed:
        server.shell(
            name="Reload NFS exports",
            commands=["exportfs -ra"],
        )

    # Enable and start NFS server
    systemd.service(
        name="Enable and start NFS server",
        service="nfs-kernel-server",
        enabled=True,
        running=True,
    )
