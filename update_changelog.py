#!/usr/bin/env python3

from pathlib import Path
import re
import subprocess

CONFIG_PATH = Path("jekyll_live/config.yaml")
CHANGELOG_PATH = Path("CHANGELOG.md")


def read_version_from_text(text: str) -> str:
    match = re.search(r"^version:\s*['\"]?([^'\"]+)['\"]?\s*$", text, re.MULTILINE)
    if not match:
        raise ValueError("Could not find version")
    return match.group(1).strip()


def read_current_version() -> str:
    return read_version_from_text(CONFIG_PATH.read_text(encoding="utf-8"))


def read_previous_version() -> str | None:
    try:
        result = subprocess.run(
            ["git", "show", f"HEAD~1:{CONFIG_PATH.as_posix()}"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return None
    return read_version_from_text(result.stdout)


def version_section_exists(changelog_text: str, version: str) -> bool:
    return re.search(rf"^##\s+{re.escape(version)}\s*$", changelog_text, re.MULTILINE) is not None


def add_version_section(changelog_text: str, version: str) -> str:
    if not changelog_text.strip():
        changelog_text = "# Changelog\n\n"

    if version_section_exists(changelog_text, version):
        return changelog_text

    new_section = f"## {version}\n\n- \n\n"

    if changelog_text.startswith("# Changelog"):
        rest = changelog_text[len("# Changelog"):].lstrip("\n")
        return f"# Changelog\n\n{new_section}{rest}"

    return f"# Changelog\n\n{new_section}{changelog_text.lstrip()}"


def main() -> None:
    current_version = read_current_version()
    previous_version = read_previous_version()

    if previous_version == current_version:
        print(f"Version unchanged ({current_version}); changelog not modified.")
        return

    changelog_text = (
        CHANGELOG_PATH.read_text(encoding="utf-8")
        if CHANGELOG_PATH.exists()
        else ""
    )

    updated = add_version_section(changelog_text, current_version)
    CHANGELOG_PATH.write_text(updated, encoding="utf-8")
    print(f"Added changelog section for new version {current_version}")


if __name__ == "__main__":
    main()
