"""Reporting-scale normalization helpers."""

from __future__ import annotations

import math
from typing import Any

from .field_codes import REPORTING_SCALE_FACTORS


def get_scale_factor(scale: str) -> int:
    if scale not in REPORTING_SCALE_FACTORS:
        raise ValueError(f"Invalid reporting scale: {scale}")
    return REPORTING_SCALE_FACTORS[scale]


def normalize_value(value: Any, scale: str) -> float | None:
    if value is None or value == "":
        return None
    number = float(value)
    if math.isnan(number):
        return None
    return number * get_scale_factor(scale)


def is_valid_scale(scale: str) -> bool:
    return scale in REPORTING_SCALE_FACTORS
