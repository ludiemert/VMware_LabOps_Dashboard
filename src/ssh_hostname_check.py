"""
First SSH test for VMware LabOps.

This script connects from Windows to the Ubuntu VM
and runs the Linux command: hostname
"""

# getpass hides the passphrase while the user types it.
from getpass import getpass

# Path helps us build the Windows path to the SSH private key safely.
from pathlib import Path

# Paramiko is the library that allows Python to use SSH.
import paramiko

# Temporary VM connection settings.
# Update VM_HOST if the NAT IP changes after a VM restart.
VM_HOST = "192.168.26.129"
VM_USER = "labops"

# This is the private SSH key created on Windows.
# Path.home() means: C:\Users\user
PRIVATE_KEY_PATH = Path.home() / ".ssh" / "labops_ed25519"


def get_vm_hostname() -> str:
    """Connect to the Ubuntu VM through SSH and return its hostname."""

    # The passphrase unlocks the private key locally on Windows.
    # It is never written in the project files or sent to GitHub.
    passphrase = getpass("SSH key passphrase: ")

    # Load the Ed25519 private key created for this project.
    private_key = paramiko.Ed25519Key.from_private_key_file(
        filename=str(PRIVATE_KEY_PATH),
        password=passphrase,
    )

    # Create an SSH client and use the host key already trusted by OpenSSH.
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())

    try:
        # Open the secure connection to the Ubuntu VM as user "labops".
        client.connect(
            hostname=VM_HOST,
            username=VM_USER,
            pkey=private_key,
            timeout=10,
        )

        # Run one safe, read-only Linux command inside the VM.
        _, stdout, stderr = client.exec_command("hostname")

        # Read the command result and remove the final line break.
        hostname = stdout.read().decode().strip()
        error_message = stderr.read().decode().strip()

        # Stop with a clear message if Ubuntu returned an error.
        if error_message:
            raise RuntimeError(error_message)

        return hostname

    finally:
        # Always close the SSH connection, even if an error happens.
        client.close()


def main() -> None:
    """Run the first VMware LabOps SSH health check."""

    hostname = get_vm_hostname()
    print(f"Connected to Ubuntu VM: {hostname}")


# This block runs main() only when this file is executed directly.
if __name__ == "__main__":
    main()
