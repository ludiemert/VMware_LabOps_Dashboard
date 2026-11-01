"""
First SSH test for VMware LabOps.

This script uses the Windows SSH client to connect to the Ubuntu VM
and run the Linux command: hostname.
"""

# Path helps us build the Windows path to the SSH private key safely.
from pathlib import Path

# subprocess allows Python to execute the Windows SSH command.
import subprocess

# Temporary VM connection settings.
# Update VM_HOST if the NAT IP changes after a VM restart.
VM_HOST = "192.168.26.129"
VM_USER = "labops"

# This is the private SSH key created on Windows.
PRIVATE_KEY_PATH = Path.home() / ".ssh" / "labops_ed25519"


def get_vm_hostname() -> str:
    """Run 'hostname' in the Ubuntu VM through SSH."""

    # This is the same SSH command that we tested successfully by hand.
    ssh_command = [
        "ssh",
        "-i",
        str(PRIVATE_KEY_PATH),
        "-o",
        "IdentitiesOnly=yes",
        f"{VM_USER}@{VM_HOST}",
        "hostname",
    ]

    # stderr stays visible in the terminal, so the SSH passphrase prompt appears.
    # stdout is captured because it contains the hostname returned by Ubuntu.
    result = subprocess.run(
        ssh_command,
        text=True,
        stdout=subprocess.PIPE,
        check=False,
    )

    # A non-zero return code means that the SSH command did not complete.
    if result.returncode != 0:
        raise RuntimeError("SSH command failed. Read the message above.")

    hostname = result.stdout.strip()

    # Avoid reporting success if Ubuntu did not return a hostname.
    if not hostname:
        raise RuntimeError("Ubuntu did not return a hostname.")

    return hostname


def main() -> None:
    """Run the first VMware LabOps SSH health check."""

    try:
        hostname = get_vm_hostname()
        print(f"Connected to Ubuntu VM: {hostname}")
    except RuntimeError as error:
        print(f"Error: {error}")


# This block runs main() only when this file is executed directly.
if __name__ == "__main__":
    main()
