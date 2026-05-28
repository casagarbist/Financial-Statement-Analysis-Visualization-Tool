"""Typed records used across the analysis pipeline."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class ValidationIssue(BaseModel):
    severity: str
    template_level: str | None = None
    statement: str | None = None
    section: str | None = None
    field_code: str | None = None
    period: str | None = None
    expected_value: float | str | None = None
    actual_value: float | str | None = None
    difference: float | None = None
    message: str


class CalculationResult(BaseModel):
    calculated_value: float | None
    formula: str
    input_fields_used: list[str]
    missing_fields: list[str]
    status: str
    message: str


class RatioResult(BaseModel):
    ratio_code: str
    ratio_name: str
    formula: str
    period: str
    value: float | None
    status: str
    warning_message: str | None = None


class TrendResult(BaseModel):
    metric_code: str
    metric_name: str
    period: str
    value: float | None
    previous_period_value: float | None = None
    absolute_change: float | None = None
    percentage_change: float | None = None
    cagr: float | None = None
    status: str


class AnalysisBundle(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    company_profile: dict[str, Any]
    template_level: str
    financial_data: Any
    validation_issues: list[ValidationIssue]
    ratios: list[RatioResult]
    trends: list[TrendResult]
