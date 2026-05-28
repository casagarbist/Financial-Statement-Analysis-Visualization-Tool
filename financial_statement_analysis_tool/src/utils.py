"""Small shared helpers."""

from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_directory(path: str | Path) -> Path:
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    return target


def period_sort_key(period: str) -> tuple[int, str]:
    digits = "".join(ch for ch in str(period) if ch.isdigit())
    return (int(digits) if digits else 0, str(period))
