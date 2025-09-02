#!/usr/bin/env python3
"""
Compute normalized SHA-256 hashes for all files under `baseline_out/`.
Normalization:
- Convert CRLF to LF
- Strip trailing whitespace per line
- Ensure final newline

Writes `baseline_hashes.txt` at repo root with lines:
<sha256>  <relative_path>
"""

from __future__ import annotations

from pathlib import Path
import hashlib


def normalize_text(data: bytes) -> bytes:
    # Try to decode as UTF-8; if fails, return raw
    try:
        text = data.decode("utf-8", errors="strict")
    except Exception:
        # Binary files: hash raw bytes
        return data

    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Strip trailing whitespace on each line
    lines = [ln.rstrip() for ln in text.split("\n")]
    normalized = "\n".join(lines)
    # Ensure trailing newline
    if not normalized.endswith("\n"):
        normalized += "\n"
    return normalized.encode("utf-8")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    baseline_root = repo_root / "baseline_out"
    output_file = repo_root / "baseline_hashes.txt"

    if not baseline_root.exists():
        print(f"baseline_out not found at: {baseline_root}")
        return 1

    entries: list[tuple[str, str]] = []

    for path in sorted(baseline_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root).as_posix()
        data = path.read_bytes()
        norm = normalize_text(data)
        digest = hashlib.sha256(norm).hexdigest()
        entries.append((digest, rel))

    with output_file.open("w", encoding="utf-8") as f:
        for digest, rel in entries:
            f.write(f"{digest}  {rel}\n")

    print(f"Wrote {len(entries)} normalized hashes to {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

