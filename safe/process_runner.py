"""Safe command execution helpers.

This module intentionally demonstrates a *safer* implementation for
comparison with the vulnerable demos. It always passes argument lists with
``shell=False``, applies timeouts, captures output, checks return codes and
handles errors without invoking a shell.

No command injection is possible here because user input is never
interpolated into a shell string.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence


@dataclass
class CommandResult:
    """Outcome of a completed command."""

    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    def stdout_lines(self) -> List[str]:
        return [line for line in self.stdout.splitlines() if line]


def _run(
    argv: Sequence[str],
    timeout: Optional[float] = 10.0,
    check: bool = False,
) -> CommandResult:
    """Run *argv* as a command list and capture its output."""
    try:
        completed = subprocess.run(
            list(argv),
            shell=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return CommandResult(-1, "", f"command timed out after {timeout}s: {exc}")
    except OSError as exc:
        return CommandResult(-1, "", f"could not start command: {exc}")
    result = CommandResult(completed.returncode, completed.stdout, completed.stderr)
    if check and not result.ok:
        raise RuntimeError(
            f"command failed ({result.returncode}): {result.stderr.strip()}"
        )
    return result


def is_available(executable: str) -> bool:
    """Return True when *executable* is on PATH."""
    return shutil.which(executable) is not None


def list_directory(path: str) -> CommandResult:
    """List the contents of *path* using the ``ls`` utility."""
    return _run(["ls", "-la", path])


def run_safe_utility(utility: str, *arguments: str) -> CommandResult:
    """Run a known *utility* with *arguments* passed as a list."""
    argv = [utility, *arguments]
    return _run(argv)


def collect_command_output(executable: str, *arguments: str) -> List[str]:
    """Return the trimmed stdout lines of *executable* with *arguments*."""
    result = _run([executable, *arguments], timeout=15.0, check=True)
    return result.stdout_lines()


def check_command(executable: str, *arguments: str) -> bool:
    """Return True when *executable* runs successfully with *arguments*."""
    return _run([executable, *arguments], timeout=5.0).ok


def run_with_input(argv: Sequence[str], stdin_text: str) -> CommandResult:
    """Run *argv* feeding *stdin_text* on standard input."""
    try:
        completed = subprocess.run(
            list(argv),
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=10.0,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return CommandResult(-1, "", str(exc))
    return CommandResult(completed.returncode, completed.stdout, completed.stderr)


def file_size_on_disk(path: str) -> Optional[int]:
    """Return the size in bytes of *path*, or None when unavailable."""
    if not is_available("stat"):
        return None
    result = _run(["stat", "-c", "%s", str(Path(path))])
    if not result.ok:
        return None
    try:
        return int(result.stdout.strip())
    except ValueError:
        return None


def count_lines(path: str) -> Optional[int]:
    """Return the number of lines in *path* using ``wc -l``."""
    if not Path(path).is_file():
        return None
    result = _run(["wc", "-l", str(Path(path))])
    if not result.ok:
        return None
    try:
        return int(result.stdout.split()[0])
    except (IndexError, ValueError):
        return None


if __name__ == "__main__":
    result = list_directory(".")
    print(result.returncode, len(result.stdout_lines()))