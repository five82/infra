"""Node.js installation via NVM."""

from pyinfra import host
from pyinfra.operations import server
from pyinfra.facts.files import File, Directory


def deploy(config, target_user, target_home):
    """Deploy Node.js via NVM."""

    nvm_dir = f"{target_home}/.nvm"
    nvm_sh = f"{nvm_dir}/nvm.sh"

    # Check if NVM is already installed
    nvm_installed = host.get_fact(File, nvm_sh)
    if not nvm_installed:
        server.shell(
            name="Install nvm",
            commands=[
                f"curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/{config.nvm_version}/install.sh | bash"
            ],
            _env={"HOME": target_home, "NVM_DIR": nvm_dir},
            _sudo=False,
        )

    # Check if Node.js is already installed
    node_dir = f"{nvm_dir}/versions/node"
    node_installed = host.get_fact(Directory, node_dir)
    if not node_installed:
        server.shell(
            name="Install Node.js via nvm",
            commands=[f"source {nvm_sh} && nvm install {config.nodejs_version}"],
            _env={"HOME": target_home, "NVM_DIR": nvm_dir},
            _sudo=False,
            _shell_executable="/bin/bash",
        )
