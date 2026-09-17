#!/usr/bin/env python3
"""construct.py - Entering the Matrix.

Detects whether the program is running inside a Python virtual
environment and reports on the current Python environment.
"""

import os
import site
import sys


def is_in_virtual_env() -> bool:
    """Return True if the interpreter is running inside a venv.

    Hint: compare sys.prefix against sys.base_prefix. Outside a venv
    they are identical; inside one, sys.prefix points at the venv.
    """
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def get_virtual_env_path() -> str | None:
    """Return the active venv's path, or None if not in one.

    Hint: the venv activation script sets the VIRTUAL_ENV
    environment variable.
    """
    return os.environ.get("VIRTUAL_ENV")


def get_site_packages() -> list[str]:
    """Return the current interpreter's site-packages location(s).

    Hint: site.getsitepackages() works both globally and inside a
    venv - the paths it returns just differ depending on context.
    """
    try:
        return list(site.getsitepackages())
    except AttributeError:
        # Some venv setups (e.g. certain --system-site-packages
        # configs) don't expose getsitepackages(); fall back.
        version = f"python{sys.version_info.major}.{sys.version_info.minor}"
        return [os.path.join(sys.prefix, "lib", version, "site-packages")]


def report_outside_matrix() -> None:
    """Print status + activation instructions (no venv detected)."""
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate  # On Unix")
    print("matrix_env\\Scripts\\activate     # On Windows")
    print()
    print("Then run this program again.")


def report_inside_matrix(venv_path: str) -> None:
    """Print status + package info (venv detected)."""
    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(venv_path)}")
    print(f"Environment Path: {venv_path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print()
    packages = get_site_packages()
    if len(packages) == 1:
        print(f"Package installation path:\n{packages[0]}")
    else:
        print("Package installation paths:")
        for path in packages:
            print(path)


def main() -> None:
    try:
        if is_in_virtual_env():
            venv_path = get_virtual_env_path() or sys.prefix
            report_inside_matrix(venv_path)
        else:
            report_outside_matrix()
    except Exception as exc:
        print(f"MATRIX ERROR: something corrupted the stream ({exc})")


if __name__ == "__main__":
    main()
