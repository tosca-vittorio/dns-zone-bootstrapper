from __future__ import annotations

import argparse
import os
import shutil
from dataclasses import dataclass
from pathlib import Path


SCRIPT_VERSION = "0.1.0"
SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent

ROOT_MARKERS = (
    "README.md",
    "pyproject.toml",
    "src",
)

PROTECTED_DIR_NAMES = {
    ".git",
    "tmp",
}

VENV_DIR_NAMES = {
    ".venv",
    "venv",
    "env",
    "ENV",
}

TARGET_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "htmlcov",
    ".tox",
    ".nox",
    "build",
    "dist",
}

TARGET_FILE_NAMES = {
    "coverage.xml",
}

TARGET_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
}


@dataclass(frozen=True, order=True)
class CleanupEntry:
    category: str
    path: Path
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Cleanup conservativo degli artefatti runtime repo-locali "
            "con boundary protetti e opt-in espliciti."
        )
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Applica realmente la rimozione. Senza il flag esegue solo dry-run.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostra i singoli path coinvolti.",
    )
    parser.add_argument(
        "--include-venv",
        action="store_true",
        help=(
            "Include anche la pulizia soft dentro .venv/venv/env/ENV. "
            "Di default gli ambienti virtuali restano esclusi."
        ),
    )
    parser.add_argument(
        "--skip-root-guard",
        action="store_true",
        help="Disabilita il root guard. Sconsigliato.",
    )
    return parser.parse_args()


def ensure_repo_root(skip_root_guard: bool) -> None:
    if skip_root_guard:
        return

    missing_markers = [
        marker
        for marker in ROOT_MARKERS
        if not (REPO_ROOT / marker).exists()
    ]
    if missing_markers:
        missing = ", ".join(missing_markers)
        raise SystemExit(
            f"Root guard failed: repository markers missing under {REPO_ROOT}: {missing}"
        )


def should_exclude_dir(dirname: str, include_venv: bool) -> bool:
    if dirname in PROTECTED_DIR_NAMES:
        return True
    if not include_venv and dirname in VENV_DIR_NAMES:
        return True
    return False


def is_coverage_file(path: Path) -> bool:
    return path.name == ".coverage" or path.name.startswith(".coverage.")


def is_inside_virtual_env(path: Path) -> bool:
    relative_path = path.relative_to(REPO_ROOT)
    return any(part in VENV_DIR_NAMES for part in relative_path.parts)


def classify_directory(path: Path) -> tuple[str, str] | None:
    if is_inside_virtual_env(path):
        if path.name == "__pycache__":
            return ("directory_artifacts", "__pycache__")
        return None

    if path.name in TARGET_DIR_NAMES:
        return ("directory_artifacts", path.name)
    if path.name.endswith(".egg-info"):
        return ("directory_artifacts", "egg-info")
    return None


def classify_file(path: Path) -> tuple[str, str] | None:
    if is_inside_virtual_env(path):
        if path.suffix in TARGET_FILE_SUFFIXES:
            return ("compiled_files", path.suffix)
        return None

    if path.name in TARGET_FILE_NAMES:
        return ("coverage_files", path.name)
    if is_coverage_file(path):
        return ("coverage_files", ".coverage")
    if path.suffix in TARGET_FILE_SUFFIXES:
        return ("compiled_files", path.suffix)
    return None


def collect_cleanup_entries(include_venv: bool) -> list[CleanupEntry]:
    entries: list[CleanupEntry] = []

    for root, dirnames, filenames in os.walk(REPO_ROOT, topdown=True):
        current_dir = Path(root)

        kept_dirnames: list[str] = []
        for dirname in sorted(dirnames):
            if should_exclude_dir(dirname, include_venv):
                continue

            classification = classify_directory(current_dir / dirname)
            if classification is not None:
                category, reason = classification
                entries.append(
                    CleanupEntry(
                        category=category,
                        path=current_dir / dirname,
                        reason=reason,
                    )
                )
                continue

            kept_dirnames.append(dirname)

        dirnames[:] = kept_dirnames

        for filename in sorted(filenames):
            path = current_dir / filename
            classification = classify_file(path)
            if classification is None:
                continue

            category, reason = classification
            entries.append(
                CleanupEntry(
                    category=category,
                    path=path,
                    reason=reason,
                )
            )

    return sorted(entries, key=lambda entry: (entry.category, entry.path.as_posix()))


def group_entries(entries: list[CleanupEntry]) -> list[tuple[str, list[CleanupEntry]]]:
    category_order = [
        "directory_artifacts",
        "compiled_files",
        "coverage_files",
    ]
    labels = {
        "directory_artifacts": "1) Directory artifacts",
        "compiled_files": "2) Compiled Python files",
        "coverage_files": "3) Coverage files",
    }

    grouped: list[tuple[str, list[CleanupEntry]]] = []
    for category in category_order:
        current_entries = [entry for entry in entries if entry.category == category]
        if current_entries:
            grouped.append((labels[category], current_entries))
    return grouped


def delete_entry(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
        return
    path.unlink(missing_ok=True)


def print_header(args: argparse.Namespace) -> None:
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"cleanup_runtime_artifacts.py v{SCRIPT_VERSION}")
    print(f"mode={mode}")
    print(f"repo_root={REPO_ROOT}")
    print(f"include_venv={args.include_venv}")
    print()


def print_grouped_entries(
    grouped_entries: list[tuple[str, list[CleanupEntry]]],
    *,
    verbose: bool,
    apply: bool,
) -> None:
    show_paths = verbose or not apply

    for section_title, section_entries in grouped_entries:
        print(section_title)
        print(f"   -> items: {len(section_entries)}")
        if show_paths:
            for entry in section_entries:
                print(f"      - {entry.path.relative_to(REPO_ROOT)}")
        print()


def main() -> int:
    args = parse_args()
    ensure_repo_root(skip_root_guard=args.skip_root_guard)

    entries = collect_cleanup_entries(include_venv=args.include_venv)

    print_header(args)

    if not entries:
        print("No cleanup targets found inside repo-owned boundaries.")
        return 0

    grouped_entries = group_entries(entries)
    print_grouped_entries(
        grouped_entries,
        verbose=args.verbose,
        apply=args.apply,
    )

    if not args.apply:
        print("Dry-run only. Re-run with --apply to remove the targets above.")
        print(f"items_removed_or_proposed={len(entries)}")
        return 0

    failures: list[tuple[Path, str]] = []
    removed_count = 0

    for entry in entries:
        try:
            delete_entry(entry.path)
            removed_count += 1
            if args.verbose:
                print(f"[REMOVED] {entry.path.relative_to(REPO_ROOT)}")
        except OSError as exc:
            failures.append((entry.path, str(exc)))
            print(
                f"[WARN] failed to remove {entry.path.relative_to(REPO_ROOT)}: {exc}"
            )

    print(f"items_removed_or_proposed={removed_count}")

    if failures:
        print(f"warnings={len(failures)}")
        return 1

    print("Cleanup completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
