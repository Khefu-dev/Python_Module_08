#!/usr/bin/env python3

import importlib
import sys

REQUIRED_PACKAGES = ["pandas", "numpy", "matplotlib"]
OPTIONAL_PACKAGES = ["requests"]

DESCRIPTIONS: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
    "requests": "Network access ready",
}


def check_dependencies() -> dict[str, str | None]:
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")

    status: dict[str, str | None] = {}
    for name in REQUIRED_PACKAGES + OPTIONAL_PACKAGES:
        description = DESCRIPTIONS[name]
        try:
            module = importlib.import_module(name)
            version = getattr(module, "__version__", "unknown")
            status[name] = version
            print(f"[OK] {name} ({version}) - {description}")
        except ImportError:
            status[name] = None
            print(f"[MISSING] {name} - {description}")
    return status


def print_missing_instructions() -> None:
    print("\nLOADING STATUS: Missing dependencies detected!\n")
    print("Install with pip:")
    print("  pip install -r requirements.txt\n")
    print("Or install with Poetry:")
    print("  poetry install")


def analyze_and_visualize() -> None:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    print("\nAnalyzing Matrix data...")
    np.random.seed(42)
    data = np.random.normal(loc=50, scale=15, size=1000)
    df = pd.DataFrame({"value": data})

    print(f"Processing {len(df)} data points...")
    print(df["value"].describe())

    print("Generating visualization...")
    plt.hist(df["value"], bins=30)
    plt.title("Matrix Data Distribution")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.savefig("matrix_analysis.png")
    plt.close()

    print("\nAnalysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    status = check_dependencies()
    missing_required = [
        name for name in REQUIRED_PACKAGES if status[name] is None
    ]
    if missing_required:
        print_missing_instructions()
        sys.exit(1)
    analyze_and_visualize()


if __name__ == "__main__":
    main()
