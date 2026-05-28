# Financial Statement Analysis & Visualization Tool

A private-company financial statement analysis project built around one standardized Excel workbook. It does not use ticker symbols, stock prices, public-company APIs, market data, or portfolio data. All analysis comes from the uploaded workbook.

## What It Includes

- Two user-input templates in one workbook: `Essential_Input` and `Comprehensive_Input`
- One structured table per input sheet covering Balance Sheet, Profit & Loss, and Cash Flow
- Strict internal field codes from `src/field_codes.py`
- Reporting-scale normalization for Units, Thousands, Millions, and Billions
- Validation report with Error, Warning, and Info severities
- Calculation engine, ratio engine, trend analysis, Streamlit dashboard, and Excel report export
- Sample private-company workbook in `sample_data/sample_private_company_data.xlsx`

## Quick Start

```bash
pip install -r requirements.txt
python -m src.template_generator
streamlit run app.py
```

## Test

```bash
pytest
```

## Workbook Flow

1. Download or generate `templates/financial_statement_template.xlsx`.
2. Fill either `Essential_Input` or `Comprehensive_Input`.
3. Keep field codes unchanged.
4. Upload the workbook in the Streamlit dashboard.
5. Review validation, ratios, trends, charts, and export the Excel analysis report.

If `Comprehensive_Input` has sufficient required data, it is used. Otherwise the app falls back to `Essential_Input`. If neither sheet is sufficient, validation errors are returned.
