from src.ingestion import read_financial_data
from src.ratios import calculate_ratios
from src.template_generator import generate_sample_data


def _ratio(results, code, period="FY2024"):
    return next(item for item in results if item.ratio_code == code and item.period == period)


def test_required_ratios(tmp_path):
    path = generate_sample_data(tmp_path / "sample.xlsx")
    level, df, _ = read_financial_data(path)
    ratios = calculate_ratios(df, level)
    assert round(_ratio(ratios, "current_ratio").value, 4) == 1.75
    assert round(_ratio(ratios, "quick_ratio").value, 4) == 1.05
    assert round(_ratio(ratios, "gross_profit_margin").value, 4) == round(127 / 317, 4)
    assert round(_ratio(ratios, "ebitda_margin").value, 4) == round(64 / 317, 4)
    assert round(_ratio(ratios, "net_profit_margin").value, 4) == round(32 / 317, 4)
    assert round(_ratio(ratios, "debt_to_equity_ratio").value, 4) == round((15 + 50) / 133, 4)
    assert round(_ratio(ratios, "interest_coverage_ratio").value, 4) == round(48 / 9, 4)
    assert round(_ratio(ratios, "operating_cash_flow_margin").value, 4) == round(42 / 317, 4)
    assert round(_ratio(ratios, "revenue_growth").value, 4) == round((317 - 278) / 278, 4)
