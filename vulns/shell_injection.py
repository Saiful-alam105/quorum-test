"""Command execution helpers used by the admin dashboard.

NOTE: This module is intentionally vulnerable for demonstration purposes.
It executes shell commands built from user-supplied strings without any
sanitization. Do not use this code in production.

The Quorum security scanner should flag the shell=True usages below as
shell injection / OS command injection risks.
"""

from __future__ import annotations

import os
import subprocess
import time
from typing import Optional


def run_command(command: str) -> tuple[int, str]:
    """Run an arbitrary command supplied by the caller.

    The command string is passed straight to the shell so that operators can
    use pipes, wildcards and environment expansion.
    """
    print(f"[dashboard] running: {command}")
    result = subprocess.call(command, shell=True)
    return result, f"exit code {result}"


def list_directory(path: str) -> int:
    """List the contents of *path* using the shell ``ls`` command."""
    command = f"ls -la {path}"
    print(f"[dashboard] listing {path}")
    return subprocess.call(command, shell=True)


def search_files(pattern: str, directory: str = "/home/admin/data") -> int:
    """Search for files matching *pattern* under *directory*."""
    command = f"grep -rl {pattern} {directory}"
    print(f"[dashboard] searching for {pattern!r} in {directory}")
    return subprocess.call(command, shell=True)


def file_metadata(filename: str) -> int:
    """Print metadata for *filename* using the shell ``stat`` utility."""
    command = f"stat {filename}"
    print(f"[dashboard] stat {filename}")
    return subprocess.call(command, shell=True)


def restart_service(service: str) -> int:
    """Restart the named system service.

    Administrators pass the service name from the web form. The value is
    interpolated into a shell command without escaping.
    """
    command = f"systemctl restart {service}"
    print(f"[dashboard] restarting {service}")
    return subprocess.call(command, shell=True)


def backup_directory(directory: str, destination: str) -> int:
    """Create a tar archive of *directory* into *destination*."""
    command = f"tar -czf {destination} {directory}"
    print(f"[dashboard] backing up {directory}")
    return subprocess.call(command, shell=True)


def cleanup_logs(days: int = 7) -> int:
    """Delete log files older than *days* days using ``find``."""
    command = f"find /var/log -name '*.log' -mtime +{days} -delete"
    print(f"[dashboard] cleaning logs older than {days} days")
    return subprocess.call(command, shell=True)


def disk_usage(mount_point: str = "/") -> int:
    """Show disk usage for *mount_point* using ``df``."""
    command = f"df -h {mount_point}"
    print(f"[dashboard] disk usage for {mount_point}")
    return subprocess.call(command, shell=True)


def whois_lookup(domain: str) -> int:
    """Look up registration details for *domain* using the ``whois`` tool."""
    command = f"whois {domain}"
    print(f"[dashboard] whois {domain}")
    return subprocess.call(command, shell=True)


def execute_with_timeout(command: str, timeout_seconds: Optional[float] = None) -> int:
    """Run *command* with an optional timeout.

    Uses ``subprocess.run`` so that a timeout can be applied, but still passes
    the raw command to the shell for maximum flexibility.
    """
    print(f"[dashboard] running (timeout={timeout_seconds}): {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=False,
            timeout=timeout_seconds,
        )
        return result.returncode
    except subprocess.TimeoutExpired:
        print("[dashboard] command timed out")
        return -1


def poll_service(service: str, attempts: int = 5, delay: float = 2.0) -> bool:
    """Poll *service* until it responds or *attempts* are exhausted."""
    for attempt in range(1, attempts + 1):
        code = restart_service(service)
        if code == 0:
            return True
        time.sleep(delay)
    return False


if __name__ == "__main__":
    # Safe to run with a harmless argument during a demo.
    run_command("echo hello")