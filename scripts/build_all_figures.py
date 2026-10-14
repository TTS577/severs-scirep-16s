#!/usr/bin/env python
"""Run all figure-generation scripts."""

from pathlib import Path
import subprocess
import sys


FIGURE_DIR = Path(__file__).resolve().parents[1] / "figures" / "scripts"


def main() -> None:
    for script in sorted(FIGURE_DIR.glob("*.py")):
        print(f"Running {script}")
        subprocess.check_call([sys.executable, str(script)])


if __name__ == "__main__":
    main()
