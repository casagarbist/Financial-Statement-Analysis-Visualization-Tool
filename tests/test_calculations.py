from src.calculations import (
    calculate_closing_cash_balance,
    calculate_ebitda,
    calculate_gross_profit,
    calculate_net_change_in_cash,
    calculate_net_profit,
    calculate_operating_profit,
    calculate_profit_before_tax,
    calculate_total_assets,
    calculate_total_equity,
    calculate_total_liabilities,
)
from src.field_codes import FC, TEMPLATE_ESSENTIAL


DATA = {
    FC.revenue: 100,
    FC.cost_of_goods_sold: 60,
    FC.gross_profit: 40,
    FC.operating_expenses_excluding_depreciation_and_amortization: 15,
    FC.ebitda: 25,
    FC.depreciation_and_amortization: 5,
    FC.operating_profit: 20,
    FC.interest_income: 2,
    FC.finance_costs: 4,
    FC.profit_before_tax: 18,
    FC.tax_expense: 5,
    FC.total_current_assets: 50,
    FC.total_non_current_assets: 70,
    FC.total_current_liabilities: 30,
    FC.total_non_current_liabilities: 40,
    FC.share_capital: 20,
    FC.retained_earnings: 25,
    FC.other_equity: 5,
    FC.net_cash_flow_from_operating_activities: 12,
    FC.net_cash_flow_from_investing_activities: -4,
    FC.net_cash_flow_from_financing_activities: 2,
    FC.net_change_in_cash: 10,
    FC.opening_cash_balance: 8,
}


def test_profit_and_balance_calculations():
    assert calculate_gross_profit(DATA, TEMPLATE_ESSENTIAL).calculated_value == 40
    assert calculate_ebitda(DATA, TEMPLATE_ESSENTIAL).calculated_value == 25
    assert calculate_operating_profit(DATA, TEMPLATE_ESSENTIAL).calculated_value == 20
    assert calculate_profit_before_tax(DATA, TEMPLATE_ESSENTIAL).calculated_value == 18
    assert calculate_net_profit(DATA, TEMPLATE_ESSENTIAL).calculated_value == 13
    assert calculate_total_assets(DATA, TEMPLATE_ESSENTIAL).calculated_value == 120
    assert calculate_total_liabilities(DATA, TEMPLATE_ESSENTIAL).calculated_value == 70
    assert calculate_total_equity(DATA, TEMPLATE_ESSENTIAL).calculated_value == 50


def test_cash_flow_calculations():
    assert calculate_net_change_in_cash(DATA, TEMPLATE_ESSENTIAL).calculated_value == 10
    assert calculate_closing_cash_balance(DATA, TEMPLATE_ESSENTIAL).calculated_value == 18
