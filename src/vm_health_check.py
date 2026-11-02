"""
VM health check for VMware LabOps.

This script runs read-only Linux diagnostic commands in the Ubuntu VM
through the Windows SSH client.
"""

# Path helps us build the Windows path to the SSH private key safely.
from pathlib import Path

# subprocess allows Python to run the Windows SSH command.
import subprocess

# Update this value if the NAT IP changes after a VM restart.
VM_HOST = "192.168.26.129"
VM_USER = "labops"

# Private key stored only on Windows.
PRIVATE_KEY_PATH = Path.home() / ".ssh" / "labops_ed25519"

# These Linux commands are safe: they only read VM information.
HEALTH_CHECK_COMMAND = """
echo '=== VM identity ==='
hostname
whoami

echo '=== Uptime and CPU ==='
uptime -p
echo -n 'CPU cores: '
nproc

echo '=== Memory ==='
free -h

echo '=== Root disk ==='
df -h /

echo '=== SSH service ==='
systemctl is-active ssh
"""


def run_vm_health_check() -> str:
    """Connect through SSH and return the diagnostic output from Ubuntu."""

    # Python starts the same SSH client that we tested manually.
    ssh_command = [
        "ssh",
        "-i",
        str(PRIVATE_KEY_PATH),
        "-o",
        "IdentitiesOnly=yes",
        f"{VM_USER}@{VM_HOST}",
        HEALTH_CHECK_COMMAND,
    ]

    # stderr remains visible, so the SSH passphrase prompt appears normally.
    # stdout is captured because it contains the Ubuntu diagnostic results.
    result = subprocess.run(
        ssh_command,
        text=True,
        stdout=subprocess.PIPE,
        check=False,
    )

    # Any non-zero code means SSH or a remote command failed.
    if result.returncode != 0:
        raise RuntimeError("Health check failed. Read the message above.")

    output = result.stdout.strip()

    if not output:
        raise RuntimeError("The Ubuntu VM did not return health-check data.")

    return output


def main() -> None:
    """Run and display the first VMware LabOps health check."""

    print("Starting VMware LabOps health check...\n")

    try:
        health_data = run_vm_health_check()
        print(health_data)
    except RuntimeError as error:
        print(f"Error: {error}")


# Run main() only when this file is executed directly.
if __name__ == "__main__":
    main()
