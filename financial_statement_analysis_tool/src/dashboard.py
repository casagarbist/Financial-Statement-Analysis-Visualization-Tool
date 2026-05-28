"""Streamlit dashboard for the financial statement analysis workflow."""

from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
import plotly.express as px
import streamlit as st

from .field_codes import FC, TEMPLATE_COMPREHENSIVE, TOOL_TITLE
from .ingestion import read_financial_data
from .ratios import calculate_ratios
from .reporting import generate_excel_report
from .template_generator import generate_template
from .trends import calculate_trends
from .validation import validate_workbook


def _field_chart(df: pd.DataFrame, field_code: str, title: str):
    subset = df[df["field_code"] == field_code].dropna(subset=["normalized_value"])
    if subset.empty:
        return None
    return px.line(subset, x="period", y="normalized_value", markers=True, title=title)


def _ratio_chart(ratios_df: pd.DataFrame, ratio_code: str, title: str):
    subset = ratios_df[(ratios_df["ratio_code"] == ratio_code) & ratios_df["value"].notna()]
    if subset.empty:
        return None
    return px.line(subset, x="period", y="value", markers=True, title=title)


def _summary_table(df: pd.DataFrame, statement: str) -> pd.DataFrame:
    subset = df[df["statement"] == statement]
    if subset.empty:
        return pd.DataFrame()
    return subset.pivot_table(index=["section", "field_code", "standard_field_name"], columns="period", values="normalized_value", aggfunc="first").reset_index()


def render_dashboard() -> None:
    st.set_page_config(page_title=TOOL_TITLE, layout="wide")
    st.title(TOOL_TITLE)

    st.header("Template download")
    template_path = generate_template()
    st.download_button("Download standardized Excel template", data=Path(template_path).read_bytes(), file_name="financial_statement_template.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.header("File upload")
    uploaded = st.file_uploader("Upload completed Excel workbook", type=["xlsx"])
    if uploaded is None:
        st.info("Upload a completed workbook to run validation, analysis, dashboard charts, and report export.")
        return

    with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded.getvalue())
        workbook_path = tmp.name

    issues, detected_level = validate_workbook(workbook_path)
    template_level, data, profile = read_financial_data(workbook_path, detected_level)
    if template_level is None:
        st.error("No input sheet has sufficient required data.")
        st.dataframe(pd.DataFrame([issue.model_dump() for issue in issues]))
        return

    ratios = calculate_ratios(data, template_level)
    trends = calculate_trends(data, ratios)
    ratios_df = pd.DataFrame([item.model_dump() for item in ratios])

    st.header(profile.get("Company Name") or "Company header")
    cols = st.columns(5)
    cols[0].metric("Template level detected", template_level)
    cols[1].metric("Reporting scale", profile.get("Reporting Scale"))
    cols[2].metric("Base currency", profile.get("Base Currency"))
    cols[3].metric("Analysis start", profile.get("Analysis Start Period"))
    cols[4].metric("Analysis end", profile.get("Analysis End Period"))

    st.header("Validation summary")
    issue_df = pd.DataFrame([issue.model_dump() for issue in issues])
    st.dataframe(issue_df, use_container_width=True)

    st.header("Balance Sheet summary")
    st.dataframe(_summary_table(data, "Balance Sheet"), use_container_width=True)
    st.header("Profit & Loss summary")
    st.dataframe(_summary_table(data, "Profit & Loss"), use_container_width=True)
    st.header("Cash Flow summary")
    st.dataframe(_summary_table(data, "Cash Flow"), use_container_width=True)

    st.header("Key ratio cards")
    latest_period = sorted(data["period"].astype(str).unique())[-1]
    for row in st.columns(4):
        pass
    key_codes = ["current_ratio", "gross_profit_margin", "net_profit_margin", "debt_to_equity_ratio"]
    metric_cols = st.columns(len(key_codes))
    for col, code in zip(metric_cols, key_codes):
        latest = ratios_df[(ratios_df["ratio_code"] == code) & (ratios_df["period"] == latest_period)]
        col.metric(code.replace("_", " ").title(), "n/a" if latest.empty or pd.isna(latest.iloc[0]["value"]) else f"{latest.iloc[0]['value']:.2f}")

    st.header("Liquidity analysis")
    st.dataframe(ratios_df[ratios_df["ratio_code"].isin(["current_ratio", "quick_ratio", "cash_ratio", "working_capital"])], use_container_width=True)
    st.header("Profitability analysis")
    st.dataframe(ratios_df[ratios_df["ratio_code"].str.contains("margin|return_on")], use_container_width=True)
    st.header("Leverage analysis")
    st.dataframe(ratios_df[ratios_df["ratio_code"].isin(["debt_to_equity_ratio", "debt_ratio", "equity_ratio", "interest_coverage_ratio", "net_debt_to_ebitda"])], use_container_width=True)
    if template_level == TEMPLATE_COMPREHENSIVE:
        st.header("Efficiency analysis")
        st.dataframe(ratios_df[ratios_df["ratio_code"].str.contains("turnover|days_|cash_conversion_cycle|asset_turnover")], use_container_width=True)
    st.header("Cash flow analysis")
    st.dataframe(ratios_df[ratios_df["ratio_code"].str.contains("cash|free_cash_flow|operating_cash_flow")], use_container_width=True)

    st.header("Trend charts")
    chart_specs = [
        (FC.revenue, "Revenue trend"),
        (FC.gross_profit, "Gross profit trend"),
        (FC.ebitda, "EBITDA trend"),
        (FC.operating_profit, "Operating profit trend"),
        (FC.net_profit, "Net profit trend"),
        (FC.total_assets, "Total assets trend"),
        (FC.total_liabilities, "Total liabilities trend"),
        (FC.total_equity, "Total equity trend"),
        (FC.net_cash_flow_from_operating_activities, "Operating cash flow trend"),
    ]
    for left, right in zip(chart_specs[::2], chart_specs[1::2]):
        col1, col2 = st.columns(2)
        fig1 = _field_chart(data, left[0], left[1])
        fig2 = _field_chart(data, right[0], right[1])
        if fig1:
            col1.plotly_chart(fig1, use_container_width=True)
        if fig2:
            col2.plotly_chart(fig2, use_container_width=True)
    for code, title in [("current_ratio", "Current ratio trend"), ("debt_to_equity_ratio", "Debt-to-equity trend"), ("net_profit_margin", "Net profit margin trend")]:
        fig = _ratio_chart(ratios_df, code, title)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    st.header("Warning messages")
    st.dataframe(issue_df[issue_df["severity"].isin(["Warning", "Error"])], use_container_width=True)

    st.header("Excel report download")
    report_bytes = generate_excel_report(profile, template_level, data, issues, ratios, trends)
    st.download_button("Download Excel analysis report", data=report_bytes, file_name="financial_statement_analysis_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
