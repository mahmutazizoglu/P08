#!/usr/bin/env python3
"""loading.py - Loading Programs.

Demonstrates package/dependency management (pip vs Poetry) while
running a small "Matrix data" analysis pipeline: simulate data with
numpy, manipulate it with pandas, visualize it with matplotlib.
"""

import importlib
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd


# Packages this program depends on. Mapped name -> import name, since
# they can differ (not the case here, but keeps this general).
REQUIRED_PACKAGES: dict[str, str] = {
    "pandas": "pandas",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
}

OPTIONAL_PACKAGES: dict[str, str] = {
    "requests": "requests",  # only needed if fetching real API data
}

DESCRIPTIONS: dict[str, str] = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
    "requests": "Network access",
}


def check_dependency(import_name: str) -> str | None:
    """Return the installed version of a package, or None if missing."""
    try:
        module = importlib.import_module(import_name)
    except ImportError:
        return None
    return getattr(module, "__version__", "unknown")


def report_dependencies() -> dict[str, str | None]:
    """Check all required + optional packages, print a status report."""
    statuses: dict[str, str | None] = {}
    for name, import_name in {
        **REQUIRED_PACKAGES,
        **OPTIONAL_PACKAGES,
    }.items():
        version = check_dependency(import_name)
        statuses[name] = version
        label = DESCRIPTIONS.get(name, "")
        if version is not None:
            print(f"[OK] {name} ({version}) - {label} ready")
        else:
            print(f"[MISSING] {name} - {label} unavailable")
    return statuses


def missing_required(statuses: dict[str, str | None]) -> list[str]:
    """Return the names of required packages that are not installed."""
    return [name for name in REQUIRED_PACKAGES if statuses.get(name) is None]


def print_installation_instructions() -> None:
    """Print pip and Poetry installation instructions."""
    print("Install with pip:")
    print("    pip install -r requirements.txt")
    print()
    print("Install with Poetry:")
    print("    poetry install")


def generate_matrix_data(n_points: int = 1000) -> "np.ndarray":
    """Generate simulated Matrix data using numpy (not hardcoded)."""
    import numpy as np

    rng = np.random.default_rng(seed=42)
    return rng.normal(loc=0.0, scale=1.0, size=n_points)


def analyze_data(data: "np.ndarray") -> "pd.DataFrame":
    """Wrap the numpy data in a pandas DataFrame and compute stats."""
    import pandas as pd

    dataframe = pd.DataFrame({"value": data})
    dataframe["rolling_mean"] = dataframe["value"].rolling(window=20).mean()
    return dataframe


def visualize(
    dataframe: "pd.DataFrame", output_path: str = "matrix_analysis.png"
) -> None:
    """Create and save a matplotlib visualization of the data."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dataframe["value"], alpha=0.4, label="raw signal")
    ax.plot(dataframe["rolling_mean"], color="green", label="rolling mean")
    ax.set_title("Matrix Data Analysis")
    ax.set_xlabel("data point")
    ax.set_ylabel("value")
    ax.legend()
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")
    statuses = report_dependencies()

    missing = missing_required(statuses)
    if missing:
        print()
        print(f"Missing required dependencies: {', '.join(missing)}")
        print_installation_instructions()
        sys.exit(1)

    print()
    print("Analyzing Matrix data...")
    data = generate_matrix_data()
    print(f"Processing {len(data)} data points...")

    dataframe = analyze_data(data)

    print("Generating visualization...")
    visualize(dataframe)

    print()
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
