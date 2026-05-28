from src.ingestion import read_financial_data
from src.ratios import calculate_ratios
from src.template_generator import generate_sample_data
from src.trends import calculate_trends


def test_trends_calculate_absolute_percentage_and_cagr(tmp_path):
    path = generate_sample_data(tmp_path / "sample.xlsx")
    level, df, _ = read_financial_data(path)
    ratios = calculate_ratios(df, level)
    trends = calculate_trends(df, ratios)
    revenue_2024 = next(item for item in trends if item.metric_code == "revenue" and item.period == "FY2024")
    assert revenue_2024.absolute_change == 39_000_000
    assert round(revenue_2024.percentage_change, 4) == round(39_000_000 / 278_000_000, 4)
    assert revenue_2024.cagr is not None
    common_size = [item for item in trends if item.metric_code == "common_size_pl_net_profit" and item.period == "FY2024"]
    assert common_size
