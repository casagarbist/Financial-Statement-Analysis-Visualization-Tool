"""Financial statement calculations based on internal field codes only."""

from __future__ import annotations

from collections.abc import Mapping
from math import isclose

from .field_codes import (
    FC,
    LINE_INPUT,
    OPTIONAL,
    TEMPLATE_ESSENTIAL,
    get_field_map,
    get_formula,
)
from .schema import CalculationResult

DATA = Mapping[str, float | int | None]


def _field_required_level(template_level: str, field_code: str) -> str | None:
    item = get_field_map(template_level).get(field_code)
    return item.required_level if item and item.line_type == LINE_INPUT else None


def _get(data: DATA, code: str, template_level: str, missing: list[str]) -> float:
    value = data.get(code)
    if value is None:
        if _field_required_level(template_level, code) == OPTIONAL:
            return 0.0
        missing.append(code)
        return 0.0
    return float(value)


def _result(value: float | None, formula: str, inputs: list[str], missing: list[str], message: str = "") -> CalculationResult:
    status = "Calculated" if not missing else "Missing Input"
    return CalculationResult(
        calculated_value=value if not missing else None,
        formula=formula,
        input_fields_used=inputs,
        missing_fields=missing,
        status=status,
        message=message or ("Calculation completed." if not missing else f"Missing required inputs: {', '.join(missing)}"),
    )


def _sum(data: DATA, template_level: str, target: str, inputs: list[str]) -> CalculationResult:
    missing: list[str] = []
    value = sum(_get(data, code, template_level, missing) for code in inputs)
    return _result(value, get_formula(template_level, target) or " + ".join(inputs), inputs, missing)


def _sub(data: DATA, template_level: str, target: str, inputs: list[str]) -> CalculationResult:
    missing: list[str] = []
    value = _get(data, inputs[0], template_level, missing)
    for code in inputs[1:]:
        value -= _get(data, code, template_level, missing)
    return _result(value, get_formula(template_level, target) or f"{inputs[0]} - {' - '.join(inputs[1:])}", inputs, missing)


def calculate_net_accounts_receivable(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    if template_level == TEMPLATE_ESSENTIAL:
        return CalculationResult(calculated_value=None, formula="Not applicable", input_fields_used=[], missing_fields=[], status="Not Applicable", message="Essential template uses accounts_receivable directly.")
    return _sub(data, template_level, FC.net_accounts_receivable, [FC.accounts_receivable, FC.allowance_for_doubtful_debts])


def calculate_net_property_plant_and_equipment(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    if template_level == TEMPLATE_ESSENTIAL:
        return CalculationResult(calculated_value=None, formula="Not applicable", input_fields_used=[], missing_fields=[], status="Not Applicable", message="Essential template uses property_plant_and_equipment directly.")
    return _sub(data, template_level, FC.net_property_plant_and_equipment, [FC.property_plant_and_equipment, FC.accumulated_depreciation])


def calculate_total_current_assets(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    if template_level == TEMPLATE_ESSENTIAL:
        fields = [FC.cash_and_cash_equivalents, FC.accounts_receivable, FC.inventory, FC.other_current_assets]
    else:
        fields = [FC.cash_and_cash_equivalents, FC.short_term_investments, FC.net_accounts_receivable, FC.inventory, FC.prepaid_expenses, FC.other_current_assets]
    return _sum(data, template_level, FC.total_current_assets, fields)


def calculate_total_non_current_assets(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    if template_level == TEMPLATE_ESSENTIAL:
        fields = [FC.property_plant_and_equipment, FC.other_non_current_assets]
    else:
        fields = [FC.net_property_plant_and_equipment, FC.intangible_assets, FC.long_term_investments, FC.deferred_tax_assets, FC.other_non_current_assets]
    return _sum(data, template_level, FC.total_non_current_assets, fields)


def calculate_total_assets(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    return _sum(data, template_level, FC.total_assets, [FC.total_current_assets, FC.total_non_current_assets])


def calculate_total_current_liabilities(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    if template_level == TEMPLATE_ESSENTIAL:
        fields = [FC.accounts_payable, FC.short_term_debt, FC.other_current_liabilities]
    else:
        fields = [FC.accounts_payable, FC.accrued_expenses, FC.short_term_debt, FC.current_portion_of_long_term_debt, FC.tax_payable, FC.other_current_liabilities]
    return _sum(data, template_level, FC.total_current_liabilities, fields)


def calculate_total_non_current_liabilities(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    if template_level == TEMPLATE_ESSENTIAL:
        fields = [FC.long_term_debt, FC.other_non_current_liabilities]
    else:
        fields = [FC.long_term_debt, FC.lease_liabilities, FC.deferred_tax_liabilities, FC.other_non_current_liabilities]
    return _sum(data, template_level, FC.total_non_current_liabilities, fields)


def calculate_total_liabilities(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    return _sum(data, template_level, FC.total_liabilities, [FC.total_current_liabilities, FC.total_non_current_liabilities])


def calculate_total_equity(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    if template_level == TEMPLATE_ESSENTIAL:
        fields = [FC.share_capital, FC.retained_earnings, FC.other_equity]
    else:
        fields = [FC.share_capital, FC.additional_paid_in_capital, FC.retained_earnings, FC.other_reserves, FC.other_equity]
    return _sum(data, template_level, FC.total_equity, fields)


def calculate_total_liabilities_and_equity(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    return _sum(data, template_level, FC.total_liabilities_and_equity, [FC.total_liabilities, FC.total_equity])


def check_balance_sheet_balances(data: DATA, template_level: str = TEMPLATE_ESSENTIAL, tolerance: float = 1.0) -> CalculationResult:
    missing: list[str] = []
    total_assets = _get(data, FC.total_assets, template_level, missing)
    total_liabilities_and_equity = _get(data, FC.total_liabilities_and_equity, template_level, missing)
    diff = total_assets - total_liabilities_and_equity
    if missing:
        status = "Missing Input"
        value = None
        message = f"Missing required inputs: {', '.join(missing)}"
    elif isclose(diff, 0.0, abs_tol=tolerance):
        status = "Calculated"
        value = diff
        message = "Balance sheet balances."
    else:
        status = "Warning"
        value = diff
        message = "Balance sheet does not balance."
    return CalculationResult(calculated_value=value, formula="total_assets - total_liabilities_and_equity", input_fields_used=[FC.total_assets, FC.total_liabilities_and_equity], missing_fields=missing, status=status, message=message)


def calculate_revenue(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    if template_level == TEMPLATE_ESSENTIAL:
        value = data.get(FC.revenue)
        return CalculationResult(calculated_value=float(value) if value is not None else None, formula=FC.revenue, input_fields_used=[FC.revenue], missing_fields=[] if value is not None else [FC.revenue], status="Calculated" if value is not None else "Missing Input", message="Essential revenue is user input.")
    return _sub(data, template_level, FC.revenue, [FC.gross_revenue, FC.sales_returns_and_allowances])


def calculate_gross_profit(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    return _sub(data, template_level, FC.gross_profit, [FC.revenue, FC.cost_of_goods_sold])


def calculate_ebitda(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    if template_level == TEMPLATE_ESSENTIAL:
        fields = [FC.gross_profit, FC.operating_expenses_excluding_depreciation_and_amortization]
    else:
        fields = [FC.gross_profit, FC.total_operating_expenses_excluding_depreciation_and_amortization]
    return _sub(data, template_level, FC.ebitda, fields)


def calculate_operating_profit(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    return _sub(data, template_level, FC.operating_profit, [FC.ebitda, FC.depreciation_and_amortization])


def calculate_profit_before_tax(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    missing: list[str] = []
    value = _get(data, FC.operating_profit, template_level, missing) + _get(data, FC.interest_income, template_level, missing) - _get(data, FC.finance_costs, template_level, missing)
    fields = [FC.operating_profit, FC.interest_income, FC.finance_costs]
    if template_level != TEMPLATE_ESSENTIAL:
        value += _get(data, FC.other_income, template_level, missing) - _get(data, FC.other_expenses, template_level, missing)
        fields += [FC.other_income, FC.other_expenses]
    return _result(value, get_formula(template_level, FC.profit_before_tax) or "profit_before_tax formula", fields, missing)


def calculate_net_profit(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    return _sub(data, template_level, FC.net_profit, [FC.profit_before_tax, FC.tax_expense])


def calculate_net_change_in_cash(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    return _sum(data, template_level, FC.net_change_in_cash, [FC.net_cash_flow_from_operating_activities, FC.net_cash_flow_from_investing_activities, FC.net_cash_flow_from_financing_activities])


def calculate_closing_cash_balance(data: DATA, template_level: str = TEMPLATE_ESSENTIAL) -> CalculationResult:
    return _sum(data, template_level, FC.closing_cash_balance, [FC.opening_cash_balance, FC.net_change_in_cash])


def check_cash_flow_reconciliation(data: DATA, template_level: str = TEMPLATE_ESSENTIAL, tolerance: float = 1.0) -> CalculationResult:
    missing: list[str] = []
    expected = _get(data, FC.opening_cash_balance, template_level, missing) + _get(data, FC.net_change_in_cash, template_level, missing)
    actual = _get(data, FC.closing_cash_balance, template_level, missing)
    diff = expected - actual
    if missing:
        return CalculationResult(calculated_value=None, formula="opening_cash_balance + net_change_in_cash - closing_cash_balance", input_fields_used=[FC.opening_cash_balance, FC.net_change_in_cash, FC.closing_cash_balance], missing_fields=missing, status="Missing Input", message=f"Missing required inputs: {', '.join(missing)}")
    return CalculationResult(calculated_value=diff, formula="opening_cash_balance + net_change_in_cash - closing_cash_balance", input_fields_used=[FC.opening_cash_balance, FC.net_change_in_cash, FC.closing_cash_balance], missing_fields=[], status="Calculated" if isclose(diff, 0.0, abs_tol=tolerance) else "Warning", message="Cash flow reconciles." if isclose(diff, 0.0, abs_tol=tolerance) else "Cash flow reconciliation mismatch.")


CALCULATION_FUNCTIONS = {
    FC.net_accounts_receivable: calculate_net_accounts_receivable,
    FC.net_property_plant_and_equipment: calculate_net_property_plant_and_equipment,
    FC.total_current_assets: calculate_total_current_assets,
    FC.total_non_current_assets: calculate_total_non_current_assets,
    FC.total_assets: calculate_total_assets,
    FC.total_current_liabilities: calculate_total_current_liabilities,
    FC.total_non_current_liabilities: calculate_total_non_current_liabilities,
    FC.total_liabilities: calculate_total_liabilities,
    FC.total_equity: calculate_total_equity,
    FC.total_liabilities_and_equity: calculate_total_liabilities_and_equity,
    FC.revenue: calculate_revenue,
    FC.gross_profit: calculate_gross_profit,
    FC.ebitda: calculate_ebitda,
    FC.operating_profit: calculate_operating_profit,
    FC.profit_before_tax: calculate_profit_before_tax,
    FC.net_profit: calculate_net_profit,
    FC.net_change_in_cash: calculate_net_change_in_cash,
    FC.closing_cash_balance: calculate_closing_cash_balance,
}
