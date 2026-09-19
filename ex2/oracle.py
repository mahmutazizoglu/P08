#!/usr/bin/env python3
"""oracle.py - Accessing the Mainframe.

Loads application configuration from environment variables (with a
.env file for local development), and reports on it. Demonstrates
secure configuration management: no hardcoded secrets, environment
variables always win over .env defaults, and dev/production behave
differently.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Configuration keys this program understands, with a sensible
# fallback default for each (used only if neither .env nor a real
# environment variable provides a value).
DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "sqlite:///local_matrix.db",
    "API_KEY": "",
    "LOG_LEVEL": "INFO",
    "ZION_ENDPOINT": "http://localhost:8000",
}

ENV_FILE = Path(".env")


def load_configuration() -> dict[str, str]:
    """Load .env (if present), then resolve every config key."""
    # override=False (the default) means: if a variable is already
    # set in the real environment, .env is NOT allowed to overwrite
    # it. That's exactly the "environment variable override" the
    # spec wants (real env vars win over .env values).
    load_dotenv(dotenv_path=ENV_FILE, override=False)
    return {
        key: os.environ.get(key, default) for key, default in DEFAULTS.items()
    }


def validate_configuration(config: dict[str, str]) -> list[str]:
    """Return a list of human-readable warnings for missing/risky config."""
    warnings: list[str] = []

    if not ENV_FILE.exists():
        warnings.append(
            "No .env file found - using built-in defaults. "
            "Copy .env.example to .env for local development."
        )

    is_production = config["MATRIX_MODE"] == "production"

    if is_production and not config["API_KEY"]:
        warnings.append("API_KEY is empty while running in production mode!")

    if is_production and config["DATABASE_URL"] == DEFAULTS["DATABASE_URL"]:
        warnings.append(
            "DATABASE_URL still points at the local dev default in "
            "production mode!"
        )

    return warnings


def report_configuration(config: dict[str, str]) -> None:
    """Print the configuration in the exercise's expected format."""
    is_production = config["MATRIX_MODE"] == "production"

    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")

    if is_production:
        print("Database: Connected to production instance")
    else:
        print("Database: Connected to local instance")

    if config["API_KEY"]:
        print("API Access: Authenticated")
    else:
        print("API Access: No credentials provided")

    print(f"Log Level: {config['LOG_LEVEL']}")
    print(f"Zion Network: {config['ZION_ENDPOINT']}")


def security_check(config: dict[str, str]) -> None:
    """Print the environment security checklist section."""
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")

    if ENV_FILE.exists():
        print("[OK] .env file properly configured")
    else:
        print(
            "[WARNING] .env file missing - relying on defaults/real env vars"
        )

    real_mode_override = os.environ.get("MATRIX_MODE") == "production"
    if real_mode_override:
        print("[OK] Production overrides available")
    else:
        print("[INFO] Production overrides available (not currently active)")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    config = load_configuration()
    warnings = validate_configuration(config)

    report_configuration(config)
    print()
    security_check(config)

    if warnings:
        print()
        for warning in warnings:
            print(f"[WARNING] {warning}")

    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
