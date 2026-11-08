"""
Structured VM health check for VMware LabOps.

This script runs Linux diagnostic commands through SSH,
converts the output into structured data and displays a readable summary.
"""

from os import environ

from pathlib import Path
import subprocess

# Update this value if the NAT IP changes after a VM restart.
VM_HOST = "192.168.26.129"
VM_USER = "labops"

# Private key stored only on the Windows host.
PRIVATE_KEY_PATH = Path.home() / ".ssh" / "labops_ed25519"

# Native Windows SSH client. It can use the Windows ssh-agent service.
WINDOWS_SSH_PATH = Path(environ["WINDIR"]) / "System32" / "OpenSSH" / "ssh.exe"

# The Ubuntu VM returns simple key=value lines.
# This format is easier for Python to read than a terminal table.
HEALTH_CHECK_COMMAND = """
echo "hostname=$(hostname)"
echo "username=$(whoami)"
echo "uptime_seconds=$(cut -d. -f1 /proc/uptime)"
echo "cpu_cores=$(nproc)"
free -b | awk '/^Mem:/ {printf "memory_total_bytes=%s\\nmemory_used_bytes=%s\\nmemory_available_bytes=%s\\n", $2, $3, $7}'
df -B1 / | awk 'NR == 2 {gsub("%", "", $5); printf "root_disk_total_bytes=%s\\nroot_disk_used_bytes=%s\\nroot_disk_available_bytes=%s\\nroot_disk_percent=%s\\n", $2, $3, $4, $5}'
echo "ssh_status=$(systemctl is-active ssh)"
"""


def run_vm_health_check() -> dict[str, str]:
    """Connect through SSH and return structured health data."""

    ssh_command = [
        str(WINDOWS_SSH_PATH),
        "-i",
        str(PRIVATE_KEY_PATH),
        "-o",
        "IdentitiesOnly=yes",
        f"{VM_USER}@{VM_HOST}",
        HEALTH_CHECK_COMMAND,
    ]

    # stdout contains the key=value data returned by Ubuntu.
    result = subprocess.run(
        ssh_command,
        text=True,
        stdout=subprocess.PIPE,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError("Health check failed. Read the message above.")

    health_data: dict[str, str] = {}

    # Each returned line has the format: key=value
    for line in result.stdout.splitlines():
        key, separator, value = line.partition("=")

        if separator:
            health_data[key] = value

    required_fields = {
        "hostname",
        "username",
        "uptime_seconds",
        "cpu_cores",
        "memory_total_bytes",
        "memory_used_bytes",
        "memory_available_bytes",
        "root_disk_total_bytes",
        "root_disk_used_bytes",
        "root_disk_percent",
        "ssh_status",
    }

    missing_fields = required_fields - health_data.keys()

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise RuntimeError(f"Ubuntu did not return: {missing}")

    return health_data


def bytes_to_gib(value_in_bytes: str) -> str:
    """Convert bytes into a readable GiB value."""

    gib = int(value_in_bytes) / (1024**3)
    return f"{gib:.1f} GiB"


def format_uptime(seconds_as_text: str) -> str:
    """Convert uptime seconds into days, hours and minutes."""

    total_seconds = int(seconds_as_text)

    days, remaining_seconds = divmod(total_seconds, 86_400)
    hours, remaining_seconds = divmod(remaining_seconds, 3_600)
    minutes, _ = divmod(remaining_seconds, 60)

    return f"{days} days, {hours} hours, {minutes} minutes"


def main() -> None:
    """Run the health check and display the structured VM summary."""

    print("Starting VMware LabOps structured health check...\n")

    try:
        health_data = run_vm_health_check()

        print("=== VMware LabOps VM Status ===")
        print(f"Hostname: {health_data['hostname']}")
        print(f"SSH user: {health_data['username']}")
        print(f"Uptime: {format_uptime(health_data['uptime_seconds'])}")
        print(f"CPU cores: {health_data['cpu_cores']}")

        print("\n=== Memory ===")
        print(f"Total: {bytes_to_gib(health_data['memory_total_bytes'])}")
        print(f"Used: {bytes_to_gib(health_data['memory_used_bytes'])}")
        print(f"Available: {bytes_to_gib(health_data['memory_available_bytes'])}")

        print("\n=== Root Disk ===")
        print(f"Total: {bytes_to_gib(health_data['root_disk_total_bytes'])}")
        print(f"Used: {bytes_to_gib(health_data['root_disk_used_bytes'])}")
        print(f"Usage: {health_data['root_disk_percent']}%")

        print("\n=== SSH Service ===")
        print(f"Status: {health_data['ssh_status']}")

    except RuntimeError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
