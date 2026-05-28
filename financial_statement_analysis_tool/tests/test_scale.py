import pytest

from src.scale import get_scale_factor, normalize_value


def test_units_conversion():
    assert normalize_value(250, "Units") == 250


def test_thousands_conversion():
    assert normalize_value(250, "Thousands") == 250_000


def test_millions_conversion():
    assert normalize_value(250, "Millions") == 250_000_000


def test_billions_conversion():
    assert normalize_value(250, "Billions") == 250_000_000_000


def test_invalid_scale_rejection():
    with pytest.raises(ValueError):
        get_scale_factor("Croissants")
