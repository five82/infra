"""Go installation from official tarball."""

from pyinfra import host
from pyinfra.operations import files, server
from pyinfra.facts.server import Command


def deploy(config):
    """Deploy Go from official tarball."""

    go_tarball = f"go{config.go_version}.linux-amd64.tar.gz"
    go_url = f"https://go.dev/dl/{go_tarball}"

    # Check installed Go version
    current_version = host.get_fact(Command, "/usr/local/go/bin/go version 2>/dev/null || echo none")
    expected = f"go version go{config.go_version}"

    if not current_version or expected not in current_version:
        # Download tarball
        files.download(
            name="Download Go tarball",
            src=go_url,
            dest=f"/tmp/{go_tarball}",
        )

        # Remove old installation and extract new one
        server.shell(
            name="Install Go",
            commands=[
                f"rm -rf /usr/local/go && tar -C /usr/local -xzf /tmp/{go_tarball}",
            ],
        )
