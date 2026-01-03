"""Samba server configuration."""

from pathlib import Path

from pyinfra import host
from pyinfra.operations import apt, files, server, systemd
from pyinfra.facts.server import Command

from secrets import smb_password


def deploy(config):
    """Deploy Samba server configuration."""

    templates_dir = Path(__file__).parent.parent / "templates"

    # Install Samba
    apt.packages(
        name="Install Samba",
        packages=["samba"],
    )

    # Ensure config include directory exists
    files.directory(
        name="Ensure Samba config include directory exists",
        path="/etc/samba/smb.conf.d",
        mode="0755",
    )

    # Add include line to smb.conf
    files.line(
        name="Ensure Samba includes daspool.conf",
        path="/etc/samba/smb.conf",
        line="   include = /etc/samba/smb.conf.d/daspool.conf",
    )

    # Deploy share config template
    samba_result = files.template(
        name="Install Samba share for daspool",
        src=str(templates_dir / "daspool.smb.conf.j2"),
        dest="/etc/samba/smb.conf.d/daspool.conf",
        user="root",
        group="root",
        mode="0644",
        samba_shares=config.samba_shares,
    )

    # Enable and start Samba services
    for service in ["smbd", "nmbd"]:
        systemd.service(
            name=f"Ensure Samba {service} is enabled and started",
            service=service,
            enabled=True,
            running=True,
            restarted=samba_result.changed,
        )

    # Check for existing Samba user
    samba_users = host.get_fact(Command, "pdbedit -L")

    # Create Samba user if not exists
    if f"{config.samba_user}:" not in (samba_users or ""):
        server.shell(
            name="Ensure Samba user exists and has password",
            commands=[
                f"printf '{smb_password}\\n{smb_password}\\n' | smbpasswd -s -a {config.samba_user}"
            ],
        )
