"""Excel analysis report export."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd

from .field_codes import TOOL_TITLE
from .schema import RatioResult, TrendResult, ValidationIssue
from .utils import ensure_directory, project_root


def _issues_df(issues: list[ValidationIssue]) -> pd.DataFrame:
    return pd.DataFrame([item.model_dump() for item in issues])


def _ratios_df(ratios: list[RatioResult]) -> pd.DataFrame:
    return pd.DataFrame([item.model_dump() for item in ratios])


def _trends_df(trends: list[TrendResult]) -> pd.DataFrame:
    return pd.DataFrame([item.model_dump() for item in trends])


def _summary_by_statement(df: pd.DataFrame, statement: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return df[df["statement"] == statement].pivot_table(index=["section", "field_code", "standard_field_name"], columns="period", values="normalized_value", aggfunc="first").reset_index()


def generate_excel_report(
    company_profile: dict[str, Any],
    template_level: str,
    financial_data: pd.DataFrame,
    validation_issues: list[ValidationIssue],
    ratios: list[RatioResult],
    trends: list[TrendResult],
    output_path: str | Path | None = None,
) -> bytes | Path:
    buffer = BytesIO() if output_path is None else None
    target = buffer if buffer is not None else Path(output_path)
    if isinstance(target, Path):
        ensure_directory(target.parent)
    with pd.ExcelWriter(target, engine="xlsxwriter") as writer:
        workbook = writer.book
        title_format = workbook.add_format({"bold": True, "font_size": 16, "font_color": "#1F4E78"})
        header_format = workbook.add_format({"bold": True, "bg_color": "#1F4E78", "font_color": "white"})
        cover = workbook.add_worksheet("Cover")
        writer.sheets["Cover"] = cover
        cover.write("A1", TOOL_TITLE, title_format)
        rows = [
            ("Company Name", company_profile.get("Company Name")),
            ("Registration Number", company_profile.get("Registration Number")),
            ("Base Currency", company_profile.get("Base Currency")),
            ("Reporting Scale", company_profile.get("Reporting Scale")),
            ("Analysis Period", f"{company_profile.get('Analysis Start Period')} to {company_profile.get('Analysis End Period')}"),
            ("Reporting Frequency", company_profile.get("Reporting Frequency")),
            ("Prepared By", company_profile.get("Prepared By")),
            ("Date of Preparation", company_profile.get("Date of Preparation")),
            ("Template Level Used", template_level),
        ]
        for idx, row in enumerate(rows, start=3):
            cover.write(idx, 0, row[0], header_format)
            cover.write(idx, 1, row[1])
        pd.DataFrame(rows, columns=["Field", "Value"]).to_excel(writer, sheet_name="Company Summary", index=False)
        _issues_df(validation_issues).to_excel(writer, sheet_name="Validation Summary", index=False)
        _summary_by_statement(financial_data, "Balance Sheet").to_excel(writer, sheet_name="Balance Sheet Summary", index=False)
        _summary_by_statement(financial_data, "Profit & Loss").to_excel(writer, sheet_name="Profit & Loss Summary", index=False)
        _summary_by_statement(financial_data, "Cash Flow").to_excel(writer, sheet_name="Cash Flow Summary", index=False)
        _ratios_df(ratios).to_excel(writer, sheet_name="Ratio Summary", index=False)
        _trends_df(trends).to_excel(writer, sheet_name="Trend Analysis", index=False)
        warning_notes = [issue.model_dump() for issue in validation_issues if issue.severity in ("Warning", "Error")]
        pd.DataFrame(warning_notes).to_excel(writer, sheet_name="Warning Notes", index=False)
        chart_sheet = workbook.add_worksheet("Charts")
        writer.sheets["Charts"] = chart_sheet
        chart_sheet.write("A1", TOOL_TITLE, title_format)
        ratios_df = _ratios_df(ratios)
        if not ratios_df.empty:
            np_margin = ratios_df[ratios_df["ratio_code"] == "net_profit_margin"][["period", "value"]].dropna()
            if not np_margin.empty:
                np_margin.to_excel(writer, sheet_name="Charts", index=False, startrow=3, startcol=0)
                chart = workbook.add_chart({"type": "line"})
                chart.add_series({"name": "Net Profit Margin", "categories": ["Charts", 4, 0, 3 + len(np_margin), 0], "values": ["Charts", 4, 1, 3 + len(np_margin), 1]})
                chart.set_title({"name": "Net Profit Margin Trend"})
                chart_sheet.insert_chart("D4", chart)
        for sheet in writer.sheets.values():
            sheet.set_column(0, 12, 18)
    if buffer is not None:
        return buffer.getvalue()
    return Path(output_path)


def generate_report_to_outputs(*args, filename: str = "financial_statement_analysis_report.xlsx", **kwargs) -> Path:
    return generate_excel_report(*args, output_path=project_root() / "outputs" / filename, **kwargs)
