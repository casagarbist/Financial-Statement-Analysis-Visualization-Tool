"""Private-company ratio engine."""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from .field_codes import FC, TEMPLATE_COMPREHENSIVE, TEMPLATE_ESSENTIAL
from .ingestion import dataframe_to_period_maps
from .schema import RatioResult
from .utils import period_sort_key
from .validation import build_calculated_period_maps


def _safe_div(numerator: float | None, denominator: float | None) -> tuple[float | None, str, str | None]:
    if numerator is None or denominator is None:
        return None, "Missing Input", "Missing input required for ratio."
    if denominator == 0:
        return None, "Division by Zero", "Denominator is zero."
    return numerator / denominator, "Calculated", None


def _avg(periods: list[str], maps: dict[str, dict[str, float]], index: int, code: str) -> float | None:
    current = maps.get(periods[index], {}).get(code)
    if current is None:
        return None
    if index == 0:
        return current
    previous = maps.get(periods[index - 1], {}).get(code)
    if previous is None:
        return current
    return (previous + current) / 2


def _growth(periods: list[str], maps: dict[str, dict[str, float]], index: int, code: str) -> tuple[float | None, str, str | None]:
    if index == 0:
        return None, "Not Applicable", "Growth requires a prior period."
    current = maps.get(periods[index], {}).get(code)
    previous = maps.get(periods[index - 1], {}).get(code)
    if current is None or previous is None:
        return None, "Missing Input", "Missing current or prior period input."
    if previous == 0:
        return None, "Division by Zero", "Prior period value is zero."
    return (current - previous) / previous, "Calculated", None


def _make(code: str, name: str, formula: str, period: str, value_status_warning: tuple[float | None, str, str | None]) -> RatioResult:
    value, status, warning = value_status_warning
    return RatioResult(ratio_code=code, ratio_name=name, formula=formula, period=period, value=value, status=status, warning_message=warning)


def calculate_ratios(df: pd.DataFrame, template_level: str = TEMPLATE_ESSENTIAL) -> list[RatioResult]:
    maps = build_calculated_period_maps(df, template_level) if not df.empty else dataframe_to_period_maps(df)
    periods = sorted(maps, key=period_sort_key)
    results: list[RatioResult] = []
    for index, period in enumerate(periods):
        data = maps[period]
        avg_assets = _avg(periods, maps, index, FC.total_assets)
        avg_equity = _avg(periods, maps, index, FC.total_equity)
        avg_ar = _avg(periods, maps, index, FC.accounts_receivable)
        avg_inventory = _avg(periods, maps, index, FC.inventory)
        avg_ap = _avg(periods, maps, index, FC.accounts_payable)
        revenue = data.get(FC.revenue)
        op_cf = data.get(FC.net_cash_flow_from_operating_activities)
        short_debt = data.get(FC.short_term_debt)
        long_debt = data.get(FC.long_term_debt)
        debt = None if short_debt is None or long_debt is None else short_debt + long_debt
        results.extend(
            [
                _make("current_ratio", "Current Ratio", "total_current_assets / total_current_liabilities", period, _safe_div(data.get(FC.total_current_assets), data.get(FC.total_current_liabilities))),
                _make("quick_ratio", "Quick Ratio", "(cash_and_cash_equivalents + accounts_receivable) / total_current_liabilities", period, _safe_div((data.get(FC.cash_and_cash_equivalents) or 0) + (data.get(FC.accounts_receivable) or 0), data.get(FC.total_current_liabilities))),
                _make("cash_ratio", "Cash Ratio", "cash_and_cash_equivalents / total_current_liabilities", period, _safe_div(data.get(FC.cash_and_cash_equivalents), data.get(FC.total_current_liabilities))),
                RatioResult(ratio_code="working_capital", ratio_name="Working Capital", formula="total_current_assets - total_current_liabilities", period=period, value=(data.get(FC.total_current_assets) - data.get(FC.total_current_liabilities)) if data.get(FC.total_current_assets) is not None and data.get(FC.total_current_liabilities) is not None else None, status="Calculated" if data.get(FC.total_current_assets) is not None and data.get(FC.total_current_liabilities) is not None else "Missing Input", warning_message=None),
                _make("gross_profit_margin", "Gross Profit Margin", "gross_profit / revenue", period, _safe_div(data.get(FC.gross_profit), revenue)),
                _make("ebitda_margin", "EBITDA Margin", "ebitda / revenue", period, _safe_div(data.get(FC.ebitda), revenue)),
                _make("operating_profit_margin", "Operating Profit Margin", "operating_profit / revenue", period, _safe_div(data.get(FC.operating_profit), revenue)),
                _make("net_profit_margin", "Net Profit Margin", "net_profit / revenue", period, _safe_div(data.get(FC.net_profit), revenue)),
                _make("return_on_assets", "Return on Assets", "net_profit / average_total_assets", period, _safe_div(data.get(FC.net_profit), avg_assets)),
                _make("return_on_equity", "Return on Equity", "net_profit / average_total_equity", period, _safe_div(data.get(FC.net_profit), avg_equity)),
                _make("debt_to_equity_ratio", "Debt-to-Equity Ratio", "(short_term_debt + long_term_debt) / total_equity", period, _safe_div(debt, data.get(FC.total_equity))),
                _make("debt_ratio", "Debt Ratio", "total_liabilities / total_assets", period, _safe_div(data.get(FC.total_liabilities), data.get(FC.total_assets))),
                _make("equity_ratio", "Equity Ratio", "total_equity / total_assets", period, _safe_div(data.get(FC.total_equity), data.get(FC.total_assets))),
                _make("interest_coverage_ratio", "Interest Coverage Ratio", "operating_profit / finance_costs", period, _safe_div(data.get(FC.operating_profit), data.get(FC.finance_costs))),
                _make("operating_cash_flow_margin", "Operating Cash Flow Margin", "net_cash_flow_from_operating_activities / revenue", period, _safe_div(op_cf, revenue)),
                _make("operating_cash_flow_to_net_profit", "Operating Cash Flow to Net Profit", "net_cash_flow_from_operating_activities / net_profit", period, _safe_div(op_cf, data.get(FC.net_profit))),
                RatioResult(ratio_code="cash_closing_reconciliation_check", ratio_name="Cash Closing Reconciliation Check", formula="opening_cash_balance + net_change_in_cash - closing_cash_balance", period=period, value=(data.get(FC.opening_cash_balance) or 0) + (data.get(FC.net_change_in_cash) or 0) - (data.get(FC.closing_cash_balance) or 0), status="Calculated", warning_message=None),
                _make("revenue_growth", "Revenue Growth", "(current_period_revenue - prior_period_revenue) / prior_period_revenue", period, _growth(periods, maps, index, FC.revenue)),
                _make("gross_profit_growth", "Gross Profit Growth", "(current_period_gross_profit - prior_period_gross_profit) / prior_period_gross_profit", period, _growth(periods, maps, index, FC.gross_profit)),
                _make("ebitda_growth", "EBITDA Growth", "(current_period_ebitda - prior_period_ebitda) / prior_period_ebitda", period, _growth(periods, maps, index, FC.ebitda)),
                _make("net_profit_growth", "Net Profit Growth", "(current_period_net_profit - prior_period_net_profit) / prior_period_net_profit", period, _growth(periods, maps, index, FC.net_profit)),
                _make("total_asset_growth", "Total Asset Growth", "(current_period_total_assets - prior_period_total_assets) / prior_period_total_assets", period, _growth(periods, maps, index, FC.total_assets)),
                _make("equity_growth", "Equity Growth", "(current_period_total_equity - prior_period_total_equity) / prior_period_total_equity", period, _growth(periods, maps, index, FC.total_equity)),
            ]
        )
        if template_level == TEMPLATE_COMPREHENSIVE:
            receivables_turnover = _safe_div(revenue, avg_ar)
            inventory_turnover = _safe_div(data.get(FC.cost_of_goods_sold), avg_inventory)
            payables_turnover = _safe_div(data.get(FC.cost_of_goods_sold), avg_ap)
            free_cash_flow = None if op_cf is None or data.get(FC.net_cash_flow_from_investing_activities) is None else op_cf + data.get(FC.net_cash_flow_from_investing_activities)
            ro_ce_denominator = None if data.get(FC.total_assets) is None or data.get(FC.total_current_liabilities) is None else data.get(FC.total_assets) - data.get(FC.total_current_liabilities)
            net_debt = None if debt is None or data.get(FC.cash_and_cash_equivalents) is None else debt - data.get(FC.cash_and_cash_equivalents)
            dso = _safe_div(365, receivables_turnover[0])
            dio = _safe_div(365, inventory_turnover[0])
            dpo = _safe_div(365, payables_turnover[0])
            ccc_value = None if dso[0] is None or dio[0] is None or dpo[0] is None else dso[0] + dio[0] - dpo[0]
            results.extend(
                [
                    _make("return_on_capital_employed", "Return on Capital Employed", "operating_profit / (total_assets - total_current_liabilities)", period, _safe_div(data.get(FC.operating_profit), ro_ce_denominator)),
                    _make("net_debt_to_ebitda", "Net Debt to EBITDA", "(short_term_debt + long_term_debt - cash_and_cash_equivalents) / ebitda", period, _safe_div(net_debt, data.get(FC.ebitda))),
                    _make("receivables_turnover", "Receivables Turnover", "revenue / average_accounts_receivable", period, receivables_turnover),
                    _make("inventory_turnover", "Inventory Turnover", "cost_of_goods_sold / average_inventory", period, inventory_turnover),
                    _make("payables_turnover", "Payables Turnover", "cost_of_goods_sold / average_accounts_payable", period, payables_turnover),
                    _make("asset_turnover", "Asset Turnover", "revenue / average_total_assets", period, _safe_div(revenue, avg_assets)),
                    _make("days_sales_outstanding", "Days Sales Outstanding", "365 / receivables_turnover", period, dso),
                    _make("days_inventory_outstanding", "Days Inventory Outstanding", "365 / inventory_turnover", period, dio),
                    _make("days_payable_outstanding", "Days Payable Outstanding", "365 / payables_turnover", period, dpo),
                    RatioResult(ratio_code="cash_conversion_cycle", ratio_name="Cash Conversion Cycle", formula="days_sales_outstanding + days_inventory_outstanding - days_payable_outstanding", period=period, value=ccc_value, status="Calculated" if ccc_value is not None else "Missing Input", warning_message=None if ccc_value is not None else "Missing turnover ratios."),
                    RatioResult(ratio_code="free_cash_flow", ratio_name="Free Cash Flow", formula="net_cash_flow_from_operating_activities + net_cash_flow_from_investing_activities", period=period, value=free_cash_flow, status="Calculated" if free_cash_flow is not None else "Missing Input", warning_message=None),
                    _make("free_cash_flow_margin", "Free Cash Flow Margin", "free_cash_flow / revenue", period, _safe_div(free_cash_flow, revenue)),
                    _make("cash_conversion_quality", "Cash Conversion Quality", "net_cash_flow_from_operating_activities / operating_profit", period, _safe_div(op_cf, data.get(FC.operating_profit))),
                ]
            )
    return results
