"""Trend and common-size analysis."""

from __future__ import annotations

import math

import pandas as pd

from .field_codes import FC, STATEMENT_BALANCE_SHEET, STATEMENT_PROFIT_LOSS
from .ratios import calculate_ratios
from .schema import RatioResult, TrendResult
from .utils import period_sort_key


def _trend_result(code: str, name: str, period: str, value: float | None, prev: float | None, first: float | None, years: int) -> TrendResult:
    if value is None:
        return TrendResult(metric_code=code, metric_name=name, period=period, value=None, previous_period_value=prev, status="Missing Input")
    absolute = None if prev is None else value - prev
    pct = None if prev in (None, 0) else absolute / prev
    cagr = None
    if first not in (None, 0) and years > 0 and value is not None and value > 0 and first and first > 0:
        cagr = math.pow(value / first, 1 / years) - 1
    return TrendResult(metric_code=code, metric_name=name, period=period, value=value, previous_period_value=prev, absolute_change=absolute, percentage_change=pct, cagr=cagr, status="Calculated")


def calculate_trends(df: pd.DataFrame, ratios: list[RatioResult] | None = None) -> list[TrendResult]:
    results: list[TrendResult] = []
    if df.empty:
        return results
    clean = df.dropna(subset=["normalized_value"]).copy()
    periods = sorted(clean["period"].astype(str).unique(), key=period_sort_key)
    for code, group in clean.groupby("field_code"):
        name = str(group["standard_field_name"].iloc[0])
        values = {str(row["period"]): float(row["normalized_value"]) for _, row in group.iterrows()}
        first_value = values.get(periods[0]) if periods else None
        for idx, period in enumerate(periods):
            results.append(_trend_result(str(code), name, period, values.get(period), values.get(periods[idx - 1]) if idx else None, first_value, idx))
    ratio_items = ratios or calculate_ratios(df, str(df["template_level"].iloc[0]))
    for ratio_code in sorted({item.ratio_code for item in ratio_items}):
        items = sorted([item for item in ratio_items if item.ratio_code == ratio_code], key=lambda item: period_sort_key(item.period))
        first_value = next((item.value for item in items if item.value is not None), None)
        for idx, item in enumerate(items):
            prev = items[idx - 1].value if idx else None
            results.append(_trend_result(item.ratio_code, item.ratio_name, item.period, item.value, prev, first_value, idx))
    for period in periods:
        period_df = clean[clean["period"].astype(str) == period]
        revenue = period_df.loc[period_df["field_code"] == FC.revenue, "normalized_value"]
        total_assets = period_df.loc[period_df["field_code"] == FC.total_assets, "normalized_value"]
        revenue_value = float(revenue.iloc[0]) if not revenue.empty else None
        assets_value = float(total_assets.iloc[0]) if not total_assets.empty else None
        for _, row in period_df.iterrows():
            if row["statement"] == STATEMENT_PROFIT_LOSS and revenue_value not in (None, 0):
                value = float(row["normalized_value"]) / revenue_value
                results.append(TrendResult(metric_code=f"common_size_pl_{row['field_code']}", metric_name=f"Common-size P&L {row['standard_field_name']}", period=period, value=value, status="Calculated"))
            if row["statement"] == STATEMENT_BALANCE_SHEET and assets_value not in (None, 0):
                value = float(row["normalized_value"]) / assets_value
                results.append(TrendResult(metric_code=f"common_size_bs_{row['field_code']}", metric_name=f"Common-size Balance Sheet {row['standard_field_name']}", period=period, value=value, status="Calculated"))
    return results
