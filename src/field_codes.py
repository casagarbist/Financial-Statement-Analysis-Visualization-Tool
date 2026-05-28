"""Single source of truth for financial statement field terminology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


TOOL_TITLE = "Financial Statement Analysis & Visualization Tool"

TEMPLATE_ESSENTIAL = "Essential"
TEMPLATE_COMPREHENSIVE = "Comprehensive"
TEMPLATE_LEVELS = (TEMPLATE_ESSENTIAL, TEMPLATE_COMPREHENSIVE)

SHEET_INSTRUCTIONS = "Instructions"
SHEET_COMPANY_PROFILE = "Company_Profile"
SHEET_ESSENTIAL_INPUT = "Essential_Input"
SHEET_COMPREHENSIVE_INPUT = "Comprehensive_Input"
SHEET_FIELD_DICTIONARY = "Field_Dictionary"
SHEET_CALCULATION_GUIDE = "Calculation_Guide"
SHEET_VALIDATION_REPORT = "Validation_Report"
REQUIRED_SHEETS = (
    SHEET_INSTRUCTIONS,
    SHEET_COMPANY_PROFILE,
    SHEET_ESSENTIAL_INPUT,
    SHEET_COMPREHENSIVE_INPUT,
    SHEET_FIELD_DICTIONARY,
    SHEET_CALCULATION_GUIDE,
    SHEET_VALIDATION_REPORT,
)

STATEMENT_BALANCE_SHEET = "Balance Sheet"
STATEMENT_PROFIT_LOSS = "Profit & Loss"
STATEMENT_CASH_FLOW = "Cash Flow"
STATEMENTS = (STATEMENT_BALANCE_SHEET, STATEMENT_PROFIT_LOSS, STATEMENT_CASH_FLOW)

LINE_INPUT = "Input"
LINE_CALCULATED = "Calculated"
LINE_CHECK = "Check"
LINE_TYPES = (LINE_INPUT, LINE_CALCULATED, LINE_CHECK)

REQUIRED = "Required"
RECOMMENDED = "Recommended"
OPTIONAL = "Optional"
REQUIRED_LEVELS = (REQUIRED, RECOMMENDED, OPTIONAL)

PROFILE_FIELDS = (
    "Company Name",
    "Registration Number",
    "Base Currency",
    "Country / Jurisdiction",
    "Reporting Frequency",
    "Financial Year End",
    "Analysis Start Period",
    "Analysis End Period",
    "Reporting Scale",
    "Prepared By",
    "Date of Preparation",
)

REPORTING_SCALE_FACTORS = {
    "Units": 1,
    "Thousands": 1_000,
    "Millions": 1_000_000,
    "Billions": 1_000_000_000,
}
REPORTING_FREQUENCIES = ("Annual", "Quarterly", "Monthly")


class FC:
    cash_and_cash_equivalents = "cash_and_cash_equivalents"
    accounts_receivable = "accounts_receivable"
    inventory = "inventory"
    other_current_assets = "other_current_assets"
    total_current_assets = "total_current_assets"
    property_plant_and_equipment = "property_plant_and_equipment"
    other_non_current_assets = "other_non_current_assets"
    total_non_current_assets = "total_non_current_assets"
    total_assets = "total_assets"
    accounts_payable = "accounts_payable"
    short_term_debt = "short_term_debt"
    other_current_liabilities = "other_current_liabilities"
    total_current_liabilities = "total_current_liabilities"
    long_term_debt = "long_term_debt"
    other_non_current_liabilities = "other_non_current_liabilities"
    total_non_current_liabilities = "total_non_current_liabilities"
    total_liabilities = "total_liabilities"
    share_capital = "share_capital"
    retained_earnings = "retained_earnings"
    other_equity = "other_equity"
    total_equity = "total_equity"
    total_liabilities_and_equity = "total_liabilities_and_equity"
    revenue = "revenue"
    cost_of_goods_sold = "cost_of_goods_sold"
    gross_profit = "gross_profit"
    operating_expenses_excluding_depreciation_and_amortization = (
        "operating_expenses_excluding_depreciation_and_amortization"
    )
    ebitda = "ebitda"
    depreciation_and_amortization = "depreciation_and_amortization"
    operating_profit = "operating_profit"
    interest_income = "interest_income"
    finance_costs = "finance_costs"
    profit_before_tax = "profit_before_tax"
    tax_expense = "tax_expense"
    net_profit = "net_profit"
    net_cash_flow_from_operating_activities = "net_cash_flow_from_operating_activities"
    net_cash_flow_from_investing_activities = "net_cash_flow_from_investing_activities"
    net_cash_flow_from_financing_activities = "net_cash_flow_from_financing_activities"
    net_change_in_cash = "net_change_in_cash"
    opening_cash_balance = "opening_cash_balance"
    closing_cash_balance = "closing_cash_balance"
    short_term_investments = "short_term_investments"
    allowance_for_doubtful_debts = "allowance_for_doubtful_debts"
    net_accounts_receivable = "net_accounts_receivable"
    prepaid_expenses = "prepaid_expenses"
    accumulated_depreciation = "accumulated_depreciation"
    net_property_plant_and_equipment = "net_property_plant_and_equipment"
    intangible_assets = "intangible_assets"
    long_term_investments = "long_term_investments"
    deferred_tax_assets = "deferred_tax_assets"
    accrued_expenses = "accrued_expenses"
    current_portion_of_long_term_debt = "current_portion_of_long_term_debt"
    tax_payable = "tax_payable"
    lease_liabilities = "lease_liabilities"
    deferred_tax_liabilities = "deferred_tax_liabilities"
    additional_paid_in_capital = "additional_paid_in_capital"
    other_reserves = "other_reserves"
    gross_revenue = "gross_revenue"
    sales_returns_and_allowances = "sales_returns_and_allowances"
    selling_expenses = "selling_expenses"
    general_and_administrative_expenses = "general_and_administrative_expenses"
    research_and_development_expenses = "research_and_development_expenses"
    other_operating_expenses = "other_operating_expenses"
    total_operating_expenses_excluding_depreciation_and_amortization = (
        "total_operating_expenses_excluding_depreciation_and_amortization"
    )
    other_income = "other_income"
    other_expenses = "other_expenses"


@dataclass(frozen=True)
class FieldDefinition:
    statement: str
    section: str
    field_code: str
    standard_field_name: str
    template_levels: tuple[str, ...]
    line_type: str
    required_level: str
    description: str
    formula: str | None = None
    used_in_ratios: tuple[str, ...] = field(default_factory=tuple)


def _fd(
    statement: str,
    section: str,
    code: str,
    name: str,
    level: str,
    line_type: str = LINE_INPUT,
    required_level: str = REQUIRED,
    description: str | None = None,
    formula: str | None = None,
    ratios: Iterable[str] = (),
) -> FieldDefinition:
    return FieldDefinition(
        statement=statement,
        section=section,
        field_code=code,
        standard_field_name=name,
        template_levels=(level,),
        line_type=line_type,
        required_level=required_level,
        description=description or name,
        formula=formula,
        used_in_ratios=tuple(ratios),
    )


def _calc(statement: str, section: str, code: str, name: str, level: str, formula: str) -> FieldDefinition:
    return _fd(statement, section, code, name, level, LINE_CALCULATED, REQUIRED, f"Calculated as {formula}", formula)


ESSENTIAL_FIELDS = [
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.cash_and_cash_equivalents, "Cash and Cash Equivalents", TEMPLATE_ESSENTIAL, ratios=("quick_ratio", "cash_ratio")),
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.accounts_receivable, "Accounts Receivable", TEMPLATE_ESSENTIAL, ratios=("quick_ratio",)),
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.inventory, "Inventory", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.other_current_assets, "Other Current Assets", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_BALANCE_SHEET, "Current Assets", FC.total_current_assets, "Total Current Assets", TEMPLATE_ESSENTIAL, "cash_and_cash_equivalents + accounts_receivable + inventory + other_current_assets"),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.property_plant_and_equipment, "Property, Plant and Equipment", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.other_non_current_assets, "Other Non-Current Assets", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.total_non_current_assets, "Total Non-Current Assets", TEMPLATE_ESSENTIAL, "property_plant_and_equipment + other_non_current_assets"),
    _calc(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.total_assets, "Total Assets", TEMPLATE_ESSENTIAL, "total_current_assets + total_non_current_assets"),
    _fd(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.accounts_payable, "Accounts Payable", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.short_term_debt, "Short-Term Debt", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.other_current_liabilities, "Other Current Liabilities", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.total_current_liabilities, "Total Current Liabilities", TEMPLATE_ESSENTIAL, "accounts_payable + short_term_debt + other_current_liabilities"),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Liabilities", FC.long_term_debt, "Long-Term Debt", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Liabilities", FC.other_non_current_liabilities, "Other Non-Current Liabilities", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_BALANCE_SHEET, "Non-Current Liabilities", FC.total_non_current_liabilities, "Total Non-Current Liabilities", TEMPLATE_ESSENTIAL, "long_term_debt + other_non_current_liabilities"),
    _calc(STATEMENT_BALANCE_SHEET, "Non-Current Liabilities", FC.total_liabilities, "Total Liabilities", TEMPLATE_ESSENTIAL, "total_current_liabilities + total_non_current_liabilities"),
    _fd(STATEMENT_BALANCE_SHEET, "Equity", FC.share_capital, "Share Capital", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_BALANCE_SHEET, "Equity", FC.retained_earnings, "Retained Earnings", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_BALANCE_SHEET, "Equity", FC.other_equity, "Other Equity", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_BALANCE_SHEET, "Equity", FC.total_equity, "Total Equity", TEMPLATE_ESSENTIAL, "share_capital + retained_earnings + other_equity"),
    _calc(STATEMENT_BALANCE_SHEET, "Equity", FC.total_liabilities_and_equity, "Total Liabilities and Equity", TEMPLATE_ESSENTIAL, "total_liabilities + total_equity"),
    _fd(STATEMENT_PROFIT_LOSS, "Revenue", FC.revenue, "Revenue", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_PROFIT_LOSS, "Cost and Gross Profit", FC.cost_of_goods_sold, "Cost of Goods Sold", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_PROFIT_LOSS, "Cost and Gross Profit", FC.gross_profit, "Gross Profit", TEMPLATE_ESSENTIAL, "revenue - cost_of_goods_sold"),
    _fd(STATEMENT_PROFIT_LOSS, "Operating Results", FC.operating_expenses_excluding_depreciation_and_amortization, "Operating Expenses Excluding Depreciation and Amortization", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_PROFIT_LOSS, "Operating Results", FC.ebitda, "EBITDA", TEMPLATE_ESSENTIAL, "gross_profit - operating_expenses_excluding_depreciation_and_amortization"),
    _fd(STATEMENT_PROFIT_LOSS, "Operating Results", FC.depreciation_and_amortization, "Depreciation and Amortization", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_PROFIT_LOSS, "Operating Results", FC.operating_profit, "Operating Profit / EBIT", TEMPLATE_ESSENTIAL, "ebitda - depreciation_and_amortization"),
    _fd(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.interest_income, "Interest Income", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.finance_costs, "Finance Costs / Interest Expense", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.profit_before_tax, "Profit Before Tax", TEMPLATE_ESSENTIAL, "operating_profit + interest_income - finance_costs"),
    _fd(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.tax_expense, "Tax Expense", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.net_profit, "Net Profit", TEMPLATE_ESSENTIAL, "profit_before_tax - tax_expense"),
    _fd(STATEMENT_CASH_FLOW, "Cash Flow", FC.net_cash_flow_from_operating_activities, "Net Cash Flow from Operating Activities", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_CASH_FLOW, "Cash Flow", FC.net_cash_flow_from_investing_activities, "Net Cash Flow from Investing Activities", TEMPLATE_ESSENTIAL),
    _fd(STATEMENT_CASH_FLOW, "Cash Flow", FC.net_cash_flow_from_financing_activities, "Net Cash Flow from Financing Activities", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_CASH_FLOW, "Cash Flow", FC.net_change_in_cash, "Net Change in Cash", TEMPLATE_ESSENTIAL, "net_cash_flow_from_operating_activities + net_cash_flow_from_investing_activities + net_cash_flow_from_financing_activities"),
    _fd(STATEMENT_CASH_FLOW, "Cash Flow", FC.opening_cash_balance, "Opening Cash Balance", TEMPLATE_ESSENTIAL),
    _calc(STATEMENT_CASH_FLOW, "Cash Flow", FC.closing_cash_balance, "Closing Cash Balance", TEMPLATE_ESSENTIAL, "opening_cash_balance + net_change_in_cash"),
]

COMPREHENSIVE_FIELDS = [
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.cash_and_cash_equivalents, "Cash and Cash Equivalents", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.short_term_investments, "Short-Term Investments", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.accounts_receivable, "Accounts Receivable", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.allowance_for_doubtful_debts, "Allowance for Doubtful Debts", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _calc(STATEMENT_BALANCE_SHEET, "Current Assets", FC.net_accounts_receivable, "Net Accounts Receivable", TEMPLATE_COMPREHENSIVE, "accounts_receivable - allowance_for_doubtful_debts"),
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.inventory, "Inventory", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.prepaid_expenses, "Prepaid Expenses", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Current Assets", FC.other_current_assets, "Other Current Assets", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _calc(STATEMENT_BALANCE_SHEET, "Current Assets", FC.total_current_assets, "Total Current Assets", TEMPLATE_COMPREHENSIVE, "cash_and_cash_equivalents + short_term_investments + net_accounts_receivable + inventory + prepaid_expenses + other_current_assets"),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.property_plant_and_equipment, "Property, Plant and Equipment", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.accumulated_depreciation, "Accumulated Depreciation", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _calc(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.net_property_plant_and_equipment, "Net Property, Plant and Equipment", TEMPLATE_COMPREHENSIVE, "property_plant_and_equipment - accumulated_depreciation"),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.intangible_assets, "Intangible Assets", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.long_term_investments, "Long-Term Investments", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.deferred_tax_assets, "Deferred Tax Assets", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.other_non_current_assets, "Other Non-Current Assets", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _calc(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.total_non_current_assets, "Total Non-Current Assets", TEMPLATE_COMPREHENSIVE, "net_property_plant_and_equipment + intangible_assets + long_term_investments + deferred_tax_assets + other_non_current_assets"),
    _calc(STATEMENT_BALANCE_SHEET, "Non-Current Assets", FC.total_assets, "Total Assets", TEMPLATE_COMPREHENSIVE, "total_current_assets + total_non_current_assets"),
    _fd(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.accounts_payable, "Accounts Payable", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.accrued_expenses, "Accrued Expenses", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.short_term_debt, "Short-Term Debt", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.current_portion_of_long_term_debt, "Current Portion of Long-Term Debt", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.tax_payable, "Tax Payable", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.other_current_liabilities, "Other Current Liabilities", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _calc(STATEMENT_BALANCE_SHEET, "Current Liabilities", FC.total_current_liabilities, "Total Current Liabilities", TEMPLATE_COMPREHENSIVE, "accounts_payable + accrued_expenses + short_term_debt + current_portion_of_long_term_debt + tax_payable + other_current_liabilities"),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Liabilities", FC.long_term_debt, "Long-Term Debt", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Liabilities", FC.lease_liabilities, "Lease Liabilities", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Liabilities", FC.deferred_tax_liabilities, "Deferred Tax Liabilities", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Non-Current Liabilities", FC.other_non_current_liabilities, "Other Non-Current Liabilities", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _calc(STATEMENT_BALANCE_SHEET, "Non-Current Liabilities", FC.total_non_current_liabilities, "Total Non-Current Liabilities", TEMPLATE_COMPREHENSIVE, "long_term_debt + lease_liabilities + deferred_tax_liabilities + other_non_current_liabilities"),
    _calc(STATEMENT_BALANCE_SHEET, "Non-Current Liabilities", FC.total_liabilities, "Total Liabilities", TEMPLATE_COMPREHENSIVE, "total_current_liabilities + total_non_current_liabilities"),
    _fd(STATEMENT_BALANCE_SHEET, "Equity", FC.share_capital, "Share Capital", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_BALANCE_SHEET, "Equity", FC.additional_paid_in_capital, "Additional Paid-In Capital", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Equity", FC.retained_earnings, "Retained Earnings", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_BALANCE_SHEET, "Equity", FC.other_reserves, "Other Reserves", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_BALANCE_SHEET, "Equity", FC.other_equity, "Other Equity", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _calc(STATEMENT_BALANCE_SHEET, "Equity", FC.total_equity, "Total Equity", TEMPLATE_COMPREHENSIVE, "share_capital + additional_paid_in_capital + retained_earnings + other_reserves + other_equity"),
    _calc(STATEMENT_BALANCE_SHEET, "Equity", FC.total_liabilities_and_equity, "Total Liabilities and Equity", TEMPLATE_COMPREHENSIVE, "total_liabilities + total_equity"),
    _fd(STATEMENT_PROFIT_LOSS, "Revenue", FC.gross_revenue, "Gross Revenue", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_PROFIT_LOSS, "Revenue", FC.sales_returns_and_allowances, "Sales Returns and Allowances", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _calc(STATEMENT_PROFIT_LOSS, "Revenue", FC.revenue, "Revenue / Net Revenue", TEMPLATE_COMPREHENSIVE, "gross_revenue - sales_returns_and_allowances"),
    _fd(STATEMENT_PROFIT_LOSS, "Cost and Gross Profit", FC.cost_of_goods_sold, "Cost of Goods Sold", TEMPLATE_COMPREHENSIVE),
    _calc(STATEMENT_PROFIT_LOSS, "Cost and Gross Profit", FC.gross_profit, "Gross Profit", TEMPLATE_COMPREHENSIVE, "revenue - cost_of_goods_sold"),
    _fd(STATEMENT_PROFIT_LOSS, "Operating Expenses", FC.selling_expenses, "Selling Expenses", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_PROFIT_LOSS, "Operating Expenses", FC.general_and_administrative_expenses, "General and Administrative Expenses", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_PROFIT_LOSS, "Operating Expenses", FC.research_and_development_expenses, "Research and Development Expenses", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_PROFIT_LOSS, "Operating Expenses", FC.other_operating_expenses, "Other Operating Expenses", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _calc(STATEMENT_PROFIT_LOSS, "Operating Expenses", FC.total_operating_expenses_excluding_depreciation_and_amortization, "Total Operating Expenses Excluding Depreciation and Amortization", TEMPLATE_COMPREHENSIVE, "selling_expenses + general_and_administrative_expenses + research_and_development_expenses + other_operating_expenses"),
    _calc(STATEMENT_PROFIT_LOSS, "Operating Expenses", FC.ebitda, "EBITDA", TEMPLATE_COMPREHENSIVE, "gross_profit - total_operating_expenses_excluding_depreciation_and_amortization"),
    _fd(STATEMENT_PROFIT_LOSS, "Operating Expenses", FC.depreciation_and_amortization, "Depreciation and Amortization", TEMPLATE_COMPREHENSIVE),
    _calc(STATEMENT_PROFIT_LOSS, "Operating Expenses", FC.operating_profit, "Operating Profit / EBIT", TEMPLATE_COMPREHENSIVE, "ebitda - depreciation_and_amortization"),
    _fd(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.interest_income, "Interest Income", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.finance_costs, "Finance Costs / Interest Expense", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.other_income, "Other Income", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _fd(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.other_expenses, "Other Expenses", TEMPLATE_COMPREHENSIVE, required_level=OPTIONAL),
    _calc(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.profit_before_tax, "Profit Before Tax", TEMPLATE_COMPREHENSIVE, "operating_profit + interest_income - finance_costs + other_income - other_expenses"),
    _fd(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.tax_expense, "Tax Expense", TEMPLATE_COMPREHENSIVE),
    _calc(STATEMENT_PROFIT_LOSS, "Non-Operating Items", FC.net_profit, "Net Profit", TEMPLATE_COMPREHENSIVE, "profit_before_tax - tax_expense"),
    _fd(STATEMENT_CASH_FLOW, "Cash Flow", FC.net_cash_flow_from_operating_activities, "Net Cash Flow from Operating Activities", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_CASH_FLOW, "Cash Flow", FC.net_cash_flow_from_investing_activities, "Net Cash Flow from Investing Activities", TEMPLATE_COMPREHENSIVE),
    _fd(STATEMENT_CASH_FLOW, "Cash Flow", FC.net_cash_flow_from_financing_activities, "Net Cash Flow from Financing Activities", TEMPLATE_COMPREHENSIVE),
    _calc(STATEMENT_CASH_FLOW, "Cash Flow", FC.net_change_in_cash, "Net Change in Cash", TEMPLATE_COMPREHENSIVE, "net_cash_flow_from_operating_activities + net_cash_flow_from_investing_activities + net_cash_flow_from_financing_activities"),
    _fd(STATEMENT_CASH_FLOW, "Cash Flow", FC.opening_cash_balance, "Opening Cash Balance", TEMPLATE_COMPREHENSIVE),
    _calc(STATEMENT_CASH_FLOW, "Cash Flow", FC.closing_cash_balance, "Closing Cash Balance", TEMPLATE_COMPREHENSIVE, "opening_cash_balance + net_change_in_cash"),
]

FIELD_DEFINITIONS_BY_TEMPLATE = {
    TEMPLATE_ESSENTIAL: ESSENTIAL_FIELDS,
    TEMPLATE_COMPREHENSIVE: COMPREHENSIVE_FIELDS,
}

INPUT_HEADERS = (
    "Statement",
    "Section",
    "Field Code",
    "Standard Field Name",
    "Line Type",
    "Required Level",
    "Description",
)

CALCULATION_GUIDE_ROWS = [
    ("Balance Sheet", "Essential Total Current Assets", "total_current_assets = cash_and_cash_equivalents + accounts_receivable + inventory + other_current_assets"),
    ("Balance Sheet", "Comprehensive Net Accounts Receivable", "net_accounts_receivable = accounts_receivable - allowance_for_doubtful_debts"),
    ("Balance Sheet", "Comprehensive Total Current Assets", "total_current_assets = cash_and_cash_equivalents + short_term_investments + net_accounts_receivable + inventory + prepaid_expenses + other_current_assets"),
    ("Balance Sheet", "Essential Total Non-Current Assets", "total_non_current_assets = property_plant_and_equipment + other_non_current_assets"),
    ("Balance Sheet", "Comprehensive Net Property, Plant and Equipment", "net_property_plant_and_equipment = property_plant_and_equipment - accumulated_depreciation"),
    ("Balance Sheet", "Comprehensive Total Non-Current Assets", "total_non_current_assets = net_property_plant_and_equipment + intangible_assets + long_term_investments + deferred_tax_assets + other_non_current_assets"),
    ("Balance Sheet", "Total Assets", "total_assets = total_current_assets + total_non_current_assets"),
    ("Balance Sheet", "Essential Total Current Liabilities", "total_current_liabilities = accounts_payable + short_term_debt + other_current_liabilities"),
    ("Balance Sheet", "Comprehensive Total Current Liabilities", "total_current_liabilities = accounts_payable + accrued_expenses + short_term_debt + current_portion_of_long_term_debt + tax_payable + other_current_liabilities"),
    ("Balance Sheet", "Essential Total Non-Current Liabilities", "total_non_current_liabilities = long_term_debt + other_non_current_liabilities"),
    ("Balance Sheet", "Comprehensive Total Non-Current Liabilities", "total_non_current_liabilities = long_term_debt + lease_liabilities + deferred_tax_liabilities + other_non_current_liabilities"),
    ("Balance Sheet", "Total Liabilities", "total_liabilities = total_current_liabilities + total_non_current_liabilities"),
    ("Balance Sheet", "Essential Total Equity", "total_equity = share_capital + retained_earnings + other_equity"),
    ("Balance Sheet", "Comprehensive Total Equity", "total_equity = share_capital + additional_paid_in_capital + retained_earnings + other_reserves + other_equity"),
    ("Balance Sheet", "Total Liabilities and Equity", "total_liabilities_and_equity = total_liabilities + total_equity"),
    ("Balance Sheet", "Balance Sheet Check", "total_assets = total_liabilities_and_equity"),
    ("Balance Sheet", "Alternative Balance Sheet Check", "total_assets = total_liabilities + total_equity"),
    ("Profit & Loss", "Comprehensive Revenue / Net Revenue", "revenue = gross_revenue - sales_returns_and_allowances"),
    ("Profit & Loss", "Gross Profit", "gross_profit = revenue - cost_of_goods_sold"),
    ("Profit & Loss", "Essential EBITDA", "ebitda = gross_profit - operating_expenses_excluding_depreciation_and_amortization"),
    ("Profit & Loss", "Comprehensive Total Operating Expenses Excluding Depreciation and Amortization", "total_operating_expenses_excluding_depreciation_and_amortization = selling_expenses + general_and_administrative_expenses + research_and_development_expenses + other_operating_expenses"),
    ("Profit & Loss", "Comprehensive EBITDA", "ebitda = gross_profit - total_operating_expenses_excluding_depreciation_and_amortization"),
    ("Profit & Loss", "Operating Profit / EBIT", "operating_profit = ebitda - depreciation_and_amortization"),
    ("Profit & Loss", "Essential Profit Before Tax", "profit_before_tax = operating_profit + interest_income - finance_costs"),
    ("Profit & Loss", "Comprehensive Profit Before Tax", "profit_before_tax = operating_profit + interest_income - finance_costs + other_income - other_expenses"),
    ("Profit & Loss", "Net Profit", "net_profit = profit_before_tax - tax_expense"),
    ("Cash Flow", "Net Change in Cash", "net_change_in_cash = net_cash_flow_from_operating_activities + net_cash_flow_from_investing_activities + net_cash_flow_from_financing_activities"),
    ("Cash Flow", "Closing Cash Balance", "closing_cash_balance = opening_cash_balance + net_change_in_cash"),
    ("Cash Flow", "Cash Flow Reconciliation Check", "opening_cash_balance + net_change_in_cash = closing_cash_balance"),
    ("Ratios", "Current Ratio", "current_ratio = total_current_assets / total_current_liabilities"),
    ("Ratios", "Debt-to-Equity Ratio", "debt_to_equity_ratio = (short_term_debt + long_term_debt) / total_equity"),
    ("Ratios", "Net Profit Margin", "net_profit_margin = net_profit / revenue"),
]


def get_fields(template_level: str) -> list[FieldDefinition]:
    return list(FIELD_DEFINITIONS_BY_TEMPLATE[template_level])


def get_field_map(template_level: str) -> dict[str, FieldDefinition]:
    return {field.field_code: field for field in get_fields(template_level)}


def get_allowed_field_codes(template_level: str) -> set[str]:
    return set(get_field_map(template_level))


def get_formula(template_level: str, field_code: str) -> str | None:
    field = get_field_map(template_level).get(field_code)
    return field.formula if field else None


def get_input_field_codes(template_level: str, required_only: bool = False) -> set[str]:
    fields = get_fields(template_level)
    return {
        item.field_code
        for item in fields
        if item.line_type == LINE_INPUT and (not required_only or item.required_level == REQUIRED)
    }
