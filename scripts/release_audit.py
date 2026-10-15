#!/usr/bin/env python3
"""Heuristic release scan of tracked/unignored files and optional complete Git history.

Does not establish consent, copyright ownership, or absence of all secrets. Review diffs too.
"""
import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKED_SUFFIX = {".png", ".jpg", ".jpeg", ".heic", ".webp", ".avif", ".zip", ".pem", ".key", ".p12"}
BLOCKED_PARTS = {"private-photos", "generated", "private-library", "personal-library", ".env", "credentials"}
PATTERNS = [re.compile(p) for p in (
    rb"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})",
    rb"sk-(?:proj-)?[A-Za-z0-9_-]{32,}",
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    rb"\x2fUsers\x2f[^/\s]+/", rb"(?:AKIA|ASIA)[A-Z0-9]{16}",
)]


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def scan(history=False):
    errors, seen, count = [], set(), 0
    def check(name, content):
        nonlocal count
        count += 1
        path = Path(name)
        if path.suffix.lower() in BLOCKED_SUFFIX or BLOCKED_PARTS.intersection(path.parts) or path.name.startswith(".env"):
            errors.append(f"disallowed public path: {name}")
        if any(pattern.search(content) for pattern in PATTERNS):
            errors.append(f"potential private data in: {name} (value withheld)")
    for name in git("ls-files", "--cached", "--others", "--exclude-standard", "-z").decode().split("\0"):
        if not name:
            continue
        path = ROOT / name
        if path.is_symlink():
            errors.append(f"symlink requires review: {name}")
        elif path.is_file():
            check(name, path.read_bytes())
    commits = git("rev-list", "--all").decode().splitlines() if history else []
    for commit in commits:
        for entry in git("ls-tree", "-rz", commit).split(b"\0"):
            if not entry:
                continue
            metadata, raw_name = entry.split(b"\t", 1)
            mode, kind, sha = metadata.split()
            name = raw_name.decode()
            if (name, sha) in seen:
                continue
            seen.add((name, sha))
            if mode != b"100644" and mode != b"100755":
                errors.append(f"non-file history entry: {name}")
            if kind == b"blob":
                check(name, git("cat-file", "blob", sha.decode()))
    if errors:
        print("\n".join(sorted(set(errors))))
        return 1
    print(f"PASS: {count} file/blob checks; {len(commits)} commits; heuristic scan only, manual diff/provenance review required")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--history", action="store_true")
    raise SystemExit(scan(p.parse_args().history))
