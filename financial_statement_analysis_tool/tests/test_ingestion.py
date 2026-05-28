from src.field_codes import TEMPLATE_COMPREHENSIVE
from src.ingestion import read_financial_data
from src.template_generator import generate_sample_data


def test_ingestion_detects_comprehensive_and_normalizes_millions(tmp_path):
    path = generate_sample_data(tmp_path / "sample.xlsx")
    level, df, profile = read_financial_data(path)
    assert level == TEMPLATE_COMPREHENSIVE
    revenue = df[(df["field_code"] == "revenue") & (df["period"] == "FY2024")]["normalized_value"].iloc[0]
    assert revenue == 317_000_000
    assert profile["Reporting Scale"] == "Millions"
