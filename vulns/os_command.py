"""Filesystem maintenance utilities built on :func:`os.system`.

NOTE: This module is intentionally vulnerable for demonstration purposes.
User-controlled strings are interpolated into commands executed through
``os.system()``. Do not use this code in production.

The Quorum security scanner should flag the ``os.system`` calls that include
untrusted input as OS command injection.
"""

from __future__ import annotations

import os
import shutil
from typing import List, Optional


def remove_path(path: str, recursive: bool = False) -> int:
    """Remove *path*. When *recursive* is set, remove directories too."""
    flag = " -r" if recursive else ""
    command = f"rm{flag} {path}"
    print(f"[fsutil] {command}")
    return os.system(command)  # noqa: S605 - intentional demo


def create_archive(source: str, archive_path: str, compress: bool = False) -> int:
    """Create a tar archive of *source* written to *archive_path*."""
    compression = "z" if compress else ""
    command = f"tar -c{compression}f {archive_path} {source}"
    print(f"[fsutil] {command}")
    return os.system(command)  # noqa: S605 - intentional demo


def check_disk_usage(mount_point: str) -> int:
    """Print disk usage for *mount_point*."""
    command = f"df -h {mount_point}"
    print(f"[fsutil] {command}")
    return os.system(command)  # noqa: S605 - intentional demo


def copy_files(source: str, destination: str, verbose: bool = False) -> int:
    """Copy files from *source* to *destination*."""
    option = " -v" if verbose else ""
    command = f"cp{option} {source} {destination}"
    print(f"[fsutil] {command}")
    return os.system(command)  # noqa: S605 - intentional demo


def clean_temporary_files(temp_dir: str, age_days: int = 3) -> int:
    """Delete temp files older than *age_days* in *temp_dir*."""
    command = f"find {temp_dir} -type f -mtime +{age_days} -delete"
    print(f"[fsutil] {command}")
    return os.system(command)  # noqa: S605 - intentional demo


def sync_directory(source: str, destination: str) -> int:
    """Mirror *source* into *destination* using ``rsync``."""
    command = f"rsync -av {source}/ {destination}/"
    print(f"[fsutil] {command}")
    return os.system(command)  # noqa: S605 - intentional demo


def chown_recursive(path: str, owner: str, group: str) -> int:
    """Change ownership of *path* recursively."""
    command = f"chown -R {owner}:{group} {path}"
    print(f"[fsutil] {command}")
    return os.system(command)  # noqa: S605 - intentional demo


def extract_archive(archive_path: str, destination: str) -> int:
    """Extract *archive_path* into *destination*."""
    command = f"tar -xzf {archive_path} -C {destination}"
    print(f"[fsutil] {command}")
    return os.system(command)  # noqa: S605 - intentional demo


def format_device_report(device: str) -> int:
    """Print a report for *device* using ``blkid``."""
    command = f"blkid {device}"
    print(f"[fsutil] {command}")
    return os.system(command)  # noqa: S605 - intentional demo


def run_multiple(commands: List[str]) -> List[int]:
    """Run several commands in sequence and return their exit codes."""
    results: List[int] = []
    for command in commands:
        print(f"[fsutil] {command}")
        results.append(os.system(command))  # noqa: S605 - intentional demo
    return results


def cleanup_with_backup(temp_dir: str, backup_dir: Optional[str] = None) -> int:
    """Remove *temp_dir*, optionally copying it to *backup_dir* first."""
    if backup_dir:
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copytree(temp_dir, f"{backup_dir}/tmp_backup", dirs_exist_ok=True)
    command = f"rm -rf {temp_dir}"
    print(f"[fsutil] {command}")
    return os.system(command)  # noqa: S605 - intentional demo


if __name__ == "__main__":
    check_disk_usage("/")