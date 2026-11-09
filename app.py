"""
VMware LabOps Dashboard.

This Streamlit app shows real health data collected from
the Ubuntu VM through SSH.
"""

# datetime creates the "last health check" timestamp.
from datetime import datetime

# Streamlit builds the web dashboard with Python.
import streamlit as st

# These functions come from our SSH health-check script.
from src.vm_health_check import (
    bytes_to_gib,
    format_uptime,
    run_vm_health_check,
)

# Configure the browser tab before creating page elements.
st.set_page_config(
    page_title="VMware LabOps Dashboard",
    page_icon="🖥️",
    layout="wide",
)


@st.cache_data(ttl=15)
def load_vm_health() -> dict[str, str]:
    """Read VM health data and cache it for 15 seconds."""

    return run_vm_health_check()


def main() -> None:
    """Build the first VMware LabOps dashboard page."""

    # Sidebar is the future navigation area of the dashboard.
    with st.sidebar:
        st.title("VMware LabOps")
        st.caption("Virtualization Lab")

        st.divider()

        st.write("🏠 Overview")
        st.write("🖥️ Virtual Machine")
        st.write("❤️ Health Checks")
        st.write("📄 Logs — planned")
        st.write("📸 Snapshots — planned")

        st.divider()
        st.caption("Windows 10 → VMware Workstation → Ubuntu")

    # Main page title and short project description.
    st.title("VMware LabOps Dashboard")
    st.caption("Real-time health data from Ubuntu Server through SSH")

    # This button clears the cached data and runs a new SSH health check.
    if st.button("Refresh health check"):
        st.cache_data.clear()

    try:
        health_data = load_vm_health()

    except RuntimeError as error:
        st.error(f"Could not collect VM health data: {error}")
        st.stop()

    # SSH active means the VM responded successfully to our health check.
    ssh_is_active = health_data["ssh_status"] == "active"
    vm_status = "Online" if ssh_is_active else "Unavailable"

    # Main VM status section.
    st.subheader("VM: labops-target")

    if ssh_is_active:
        st.success(f"{vm_status} — SSH service is active")
    else:
        st.warning(vm_status)

    # Cards with real information returned by Ubuntu.
    status_card, cpu_card, ram_card, disk_card, uptime_card = st.columns(5)

    status_card.metric("SSH status", health_data["ssh_status"])
    cpu_card.metric("CPU cores", health_data["cpu_cores"])
    ram_card.metric(
        "Memory available",
        bytes_to_gib(health_data["memory_available_bytes"]),
    )
    disk_card.metric(
        "Root disk usage",
        f"{health_data['root_disk_percent']}%",
    )
    uptime_card.metric(
        "Uptime",
        format_uptime(health_data["uptime_seconds"]),
    )

    st.divider()

    # Two columns for VM details and the real structured data.
    details_column, data_column = st.columns(2)

    with details_column:
        st.subheader("Virtual machine details")

        st.write(f"**Hostname:** {health_data['hostname']}")
        st.write(f"**SSH user:** {health_data['username']}")
        st.write("**Operating system:** Ubuntu Server 26.04.1 LTS")
        st.write("**Hypervisor:** VMware Workstation")
        st.write("**Virtual disk configured:** 20 GB")

    with data_column:
        st.subheader("Health check details")

        st.write(
            f"**Memory used:** " f"{bytes_to_gib(health_data['memory_used_bytes'])}"
        )
        st.write(
            f"**Memory total:** " f"{bytes_to_gib(health_data['memory_total_bytes'])}"
        )
        st.write(
            f"**Root disk used:** "
            f"{bytes_to_gib(health_data['root_disk_used_bytes'])}"
        )
        st.caption(
            "Last health check: " + datetime.now().strftime("%d %b %Y, %H:%M:%S")
        )

    # Useful during development: shows the exact values for future logs/API.
    with st.expander("View raw health-check data"):
        st.json(health_data)


if __name__ == "__main__":
    main()
