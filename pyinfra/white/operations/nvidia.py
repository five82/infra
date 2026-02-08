"""NVIDIA headless driver and CUDA toolkit installation."""

from pyinfra import host
from pyinfra.operations import apt, files, server
from pyinfra.facts.files import File


def deploy(config):
    """Deploy NVIDIA headless driver and CUDA toolkit from NVIDIA repos."""

    # Install kernel headers for DKMS
    apt.packages(
        name="Install kernel headers for NVIDIA DKMS",
        packages=["linux-headers-amd64"],
    )

    # Download and install CUDA keyring
    keyring_path = "/tmp/cuda-keyring.deb"
    keyring_installed = host.get_fact(
        File, "/usr/share/keyrings/cuda-archive-keyring.gpg"
    )

    if not keyring_installed:
        files.download(
            name="Download NVIDIA CUDA keyring",
            src=config.nvidia_cuda_keyring_url,
            dest=keyring_path,
        )

        server.shell(
            name="Install NVIDIA CUDA keyring",
            commands=[f"dpkg -i {keyring_path}"],
        )

        apt.update(
            name="Update apt cache after adding NVIDIA repo",
        )

    # Install headless NVIDIA driver
    apt.packages(
        name="Install NVIDIA headless driver",
        packages=config.nvidia_driver_packages,
    )

    # Install CUDA toolkit
    apt.packages(
        name="Install CUDA toolkit",
        packages=config.nvidia_cuda_packages,
    )
