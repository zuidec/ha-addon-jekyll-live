#!/usr/bin/env python3

from pathlib import Path
import re
import subprocess

CONFIG_PATH = Path("jekyll_live/config.yaml")
CHANGELOG_PATH = Path("CHANGELOG.md")


def run_git(args: list[str], check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=check,
    )
    return result.stdout


def read_version_from_text(text: str) -> str:
    match = re.search(r'^version:\s*["\']?([^"\']+)["\']?\s*$', text, re.MULTILINE)
    if not match:
        raise ValueError("Could not find version in config.yaml text")
    return match.group(1).strip()


def read_current_version() -> str:
    return read_version_from_text(CONFIG_PATH.read_text(encoding="utf-8"))


def find_previous_version_commit() -> tuple[str | None, str | None]:
    """
    Returns:
      (commit_sha, previous_version)

    Finds the most recent commit before HEAD where config.yaml had a
    different version than the current version.
    """
    current_version = read_current_version()
    history = run_git(["log", "--format=%H", "--", CONFIG_PATH.as_posix()]).splitlines()

    # Skip HEAD, start looking backward through prior revisions of config.yaml
    for commit in history[1:]:
        try:
            old_text = run_git(["show", f"{commit}:{CONFIG_PATH.as_posix()}"])
            old_version = read_version_from_text(old_text)
        except subprocess.CalledProcessError:
            continue

        if old_version != current_version:
            return commit, old_version

    return None, None


def get_commit_messages_since(commit_sha: str | None) -> list[str]:
    """
    Returns commit subjects after commit_sha up to HEAD, oldest first.
    Excludes merge commits.
    """
    if commit_sha is None:
        revspec = "HEAD"
    else:
        revspec = f"{commit_sha}..HEAD"

    output = run_git([
        "log",
        revspec,
        "--no-merges",
        "--format=%s",
        "--reverse",
    ])

    messages = [line.strip() for line in output.splitlines() if line.strip()]

    # Optionally drop the version bump commit itself if present
    filtered = [
        msg for msg in messages
        if not re.search(r'\bversion\b', msg, re.IGNORECASE)
    ]
    return filtered


def version_section_exists(changelog_text: str, version: str) -> bool:
    pattern = rf"^##\s+{re.escape(version)}\s*$"
    return re.search(pattern, changelog_text, re.MULTILINE) is not None


def ensure_header(changelog_text: str) -> str:
    if changelog_text.strip():
        return changelog_text
    return "# Changelog\n\n"


def build_version_section(version: str, messages: list[str]) -> str:
    if messages:
        bullets = "\n".join(f"- {msg}" for msg in messages)
    else:
        bullets = "-"

    return f"## {version}\n\n{bullets}\n\n"


def insert_version_section(changelog_text: str, version: str, messages: list[str]) -> str:
    changelog_text = ensure_header(changelog_text)

    if version_section_exists(changelog_text, version):
        return changelog_text

    new_section = build_version_section(version, messages)

    if changelog_text.startswith("# Changelog"):
        rest = changelog_text[len("# Changelog"):].lstrip("\n")
        return f"# Changelog\n\n{new_section}{rest}"

    return f"# Changelog\n\n{new_section}{changelog_text.lstrip()}"


def main() -> None:
    current_version = read_current_version()
    previous_commit, previous_version = find_previous_version_commit()

    messages = get_commit_messages_since(previous_commit)

    if CHANGELOG_PATH.exists():
        changelog_text = CHANGELOG_PATH.read_text(encoding="utf-8")
    else:
        changelog_text = ""

    updated = insert_version_section(changelog_text, current_version, messages)
    CHANGELOG_PATH.write_text(updated, encoding="utf-8")

    if previous_version is None:
        print(f"Created/updated changelog for {current_version} using available git history.")
    else:
        print(f"Added section for {current_version} with commits since version {previous_version}.")


if __name__ == "__main__":
    main()
