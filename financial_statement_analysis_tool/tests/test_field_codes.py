from collections import Counter

from src.field_codes import (
    COMPREHENSIVE_FIELDS,
    ESSENTIAL_FIELDS,
    LINE_CALCULATED,
    TEMPLATE_COMPREHENSIVE,
    TEMPLATE_ESSENTIAL,
    get_allowed_field_codes,
    get_fields,
)


def test_no_duplicate_field_codes_within_same_statement():
    for level in (TEMPLATE_ESSENTIAL, TEMPLATE_COMPREHENSIVE):
        keys = [(field.statement, field.field_code) for field in get_fields(level)]
        duplicates = [key for key, count in Counter(keys).items() if count > 1]
        assert duplicates == []


def test_essential_template_uses_approved_field_codes_only():
    approved = get_allowed_field_codes(TEMPLATE_ESSENTIAL)
    assert {field.field_code for field in ESSENTIAL_FIELDS} <= approved


def test_comprehensive_template_uses_approved_field_codes_only():
    approved = get_allowed_field_codes(TEMPLATE_COMPREHENSIVE)
    assert {field.field_code for field in COMPREHENSIVE_FIELDS} <= approved


def test_every_calculated_field_has_formula():
    for level in (TEMPLATE_ESSENTIAL, TEMPLATE_COMPREHENSIVE):
        calculated = [field for field in get_fields(level) if field.line_type == LINE_CALCULATED]
        assert calculated
        assert all(field.formula for field in calculated)
