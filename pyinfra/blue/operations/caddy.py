"""Caddy reverse proxy quadlet configuration."""

from pathlib import Path

from pyinfra.operations import files, systemd

from secrets import caddy_cloudflare_api_token


def deploy(config):
    """Deploy Caddy quadlet with Cloudflare DNS-01."""

    templates_dir = Path(__file__).parent.parent / "templates"

    # Validate secret
    if not caddy_cloudflare_api_token or caddy_cloudflare_api_token == "your-cloudflare-api-token-here":
        raise RuntimeError(
            "Set caddy_cloudflare_api_token in secrets.py before configuring Caddy."
        )

    # Ensure Caddy config directory exists
    files.directory(
        name="Ensure Caddy configuration directory exists",
        path="/etc/caddy",
        user="root",
        group="root",
        mode="0755",
    )

    # Deploy env file (contains secret)
    env_result = files.template(
        name="Install Caddy env file",
        src=str(templates_dir / "caddy.env.j2"),
        dest="/etc/caddy/caddy.env",
        user="root",
        group="root",
        mode="0600",
        caddy_cloudflare_api_token=caddy_cloudflare_api_token,
    )

    # Deploy Caddyfile
    caddyfile_result = files.template(
        name="Install Caddyfile",
        src=str(templates_dir / "Caddyfile.j2"),
        dest="/etc/caddy/Caddyfile",
        user="root",
        group="root",
        mode="0644",
        caddy_jellyfin_domain=config.caddy_jellyfin_domain,
        caddy_jellyfin_upstream=config.caddy_jellyfin_upstream,
    )

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
        name="Install Caddy quadlet",
        src=str(templates_dir / "caddy.container.j2"),
        dest="/etc/containers/systemd/caddy.container",
        user="root",
        group="root",
        mode="0644",
        caddy_image=config.caddy_image,
    )

    # Track if any config changed
    any_changed = env_result.changed or caddyfile_result.changed or quadlet_result.changed

    # Reload systemd if quadlet changed
    if quadlet_result.changed:
        systemd.daemon_reload(
            name="Reload systemd daemon",
        )

    # Start Caddy (quadlet units are auto-enabled via generator, cannot be manually enabled)
    systemd.service(
        name="Start Caddy",
        service="caddy.service",
        running=True,
        restarted=any_changed,
    )
