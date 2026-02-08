"""MakeMKV headless (console-only) installation from source."""

from pyinfra import host
from pyinfra.operations import apt, server
from pyinfra.facts.server import Command


def deploy(config):
    """Deploy MakeMKV built from source with --disable-gui."""

    version = config.makemkv_version
    oss_tarball = f"makemkv-oss-{version}.tar.gz"
    bin_tarball = f"makemkv-bin-{version}.tar.gz"
    oss_url = f"https://www.makemkv.com/download/{oss_tarball}"
    bin_url = f"https://www.makemkv.com/download/{bin_tarball}"

    # Check installed version via stamp file
    installed_version = host.get_fact(Command, "cat /usr/local/share/makemkv/.version 2>/dev/null || echo none")

    if installed_version != version:
        # Install build dependencies
        apt.packages(
            name="Install MakeMKV build dependencies",
            packages=config.makemkv_build_deps,
        )

        # Download source tarballs
        server.shell(
            name="Download MakeMKV source tarballs",
            commands=[
                f"curl -fSL -o /tmp/{oss_tarball} {oss_url}",
                f"curl -fSL -o /tmp/{bin_tarball} {bin_url}",
            ],
        )

        # Build and install makemkv-oss (headless)
        server.shell(
            name="Build and install makemkv-oss (headless)",
            commands=[
                f"tar -xzf /tmp/{oss_tarball} -C /tmp",
                f"cd /tmp/makemkv-oss-{version} && ./configure --disable-gui && make && make install",
            ],
        )

        # Build and install makemkv-bin
        server.shell(
            name="Build and install makemkv-bin",
            commands=[
                f"tar -xzf /tmp/{bin_tarball} -C /tmp",
                f"mkdir -p /tmp/makemkv-bin-{version}/tmp",
                f"echo accepted > /tmp/makemkv-bin-{version}/tmp/eula_accepted",
                f"cd /tmp/makemkv-bin-{version} && make install",
            ],
        )

        # Write version stamp
        server.shell(
            name="Write MakeMKV version stamp",
            commands=[
                "mkdir -p /usr/local/share/makemkv",
                f"echo {version} > /usr/local/share/makemkv/.version",
            ],
        )

        # Clean up build artifacts
        server.shell(
            name="Clean up MakeMKV build artifacts",
            commands=[
                f"rm -rf /tmp/makemkv-oss-{version} /tmp/makemkv-bin-{version}",
                f"rm -f /tmp/{oss_tarball} /tmp/{bin_tarball}",
            ],
        )
