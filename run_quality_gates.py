from __future__ import annotations

import subprocess
import sys


PYTHON = sys.executable

COMMANDS: list[list[str]] = [
    [PYTHON, "-B", "-m", "pytest", "-q"],
    [PYTHON, "-m", "pylint", "src", "tests"],
    [PYTHON, "-m", "coverage", "erase"],
    [PYTHON, "-B", "-m", "coverage", "run", "--source=dns_zone_bootstrapper", "-m", "pytest", "-q"],
    [PYTHON, "-m", "coverage", "report", "-m"],
]


def main() -> int:
    for command in COMMANDS:
        print("+", " ".join(command))
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
