import streamlit as st
import pandas as pd
import io
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Business Intelligence Reports")

# ==========================================
# LOAD DATA
# ==========================================

feature_data = st.session_state.get(
    "feature_data",
    pd.DataFrame()
)

forecast_data = st.session_state.get(
    "forecast_results",
    pd.DataFrame()
)

inventory_data = st.session_state.get(
    "inventory_results",
    pd.DataFrame()
)

summary_text = st.session_state.get(
    "executive_summary",
    "No Summary Available"
)

# ==========================================
# KPI SUMMARY
# ==========================================

st.header("📊 Executive KPI Dashboard")

total_revenue = 0
total_units = 0
forecast_total = 0
total_products = 0

if not feature_data.empty:

    if "Revenue" in feature_data.columns:
        total_revenue = feature_data["Revenue"].sum()

    if "Units_Sold" in feature_data.columns:
        total_units = feature_data["Units_Sold"].sum()

    if "Product_Name" in feature_data.columns:
        total_products = feature_data["Product_Name"].nunique()
    elif "Medicine_Name" in feature_data.columns:
        total_products = feature_data["Medicine_Name"].nunique()

if not forecast_data.empty:
    forecast_total = forecast_data[
        "Forecasted_Sales"
    ].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Units Sold",
        f"{total_units:,.0f}"
    )

with col3:
    st.metric(
        "Forecast Demand",
        f"{forecast_total:,.0f}"
    )

with col4:
    st.metric(
        "Products",
        total_products
    )

st.divider()

# ==========================================
# EXECUTIVE SUMMARY
# ==========================================

st.header("📋 Executive Summary")

st.text_area(
    "Summary",
    summary_text,
    height=250
)

st.divider()

# ==========================================
# FORECAST REPORT
# ==========================================

st.header("📈 Forecast Report")

if not forecast_data.empty:

    st.dataframe(
        forecast_data,
        use_container_width=True
    )

else:
    st.info(
        "Forecast data not available."
    )

st.divider()

# ==========================================
# INVENTORY REPORT
# ==========================================

st.header("📦 Inventory Report")

if not inventory_data.empty:

    st.dataframe(
        inventory_data,
        use_container_width=True
    )

else:
    st.info(
        "Inventory report not available."
    )

st.divider()

# ==========================================
# DATASET REPORT
# ==========================================

st.header("🗂 Dataset Report")

if not feature_data.empty:

    report_df = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Missing Values",
            "Duplicates"
        ],
        "Value": [
            feature_data.shape[0],
            feature_data.shape[1],
            feature_data.isnull().sum().sum(),
            feature_data.duplicated().sum()
        ]
    })

    st.dataframe(
        report_df,
        use_container_width=True
    )

else:
    st.info("Dataset not available.")

st.divider()

# ==========================================
# DOWNLOAD FORECAST CSV
# ==========================================

st.header("⬇ Download Reports")

if not forecast_data.empty:

    forecast_csv = forecast_data.to_csv(
        index=False
    )

    st.download_button(
        "Download Forecast CSV",
        forecast_csv,
        "forecast_report.csv",
        "text/csv"
    )

# ==========================================
# DOWNLOAD INVENTORY CSV
# ==========================================

if not inventory_data.empty:

    inventory_csv = inventory_data.to_csv(
        index=False
    )

    st.download_button(
        "Download Inventory CSV",
        inventory_csv,
        "inventory_report.csv",
        "text/csv"
    )

# ==========================================
# DOWNLOAD COMPLETE EXCEL REPORT
# ==========================================

if st.button(
    "Generate Excel Report"
):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        if not feature_data.empty:
            feature_data.to_excel(
                writer,
                sheet_name="Dataset",
                index=False
            )

        if not forecast_data.empty:
            forecast_data.to_excel(
                writer,
                sheet_name="Forecast",
                index=False
            )

        if not inventory_data.empty:
            inventory_data.to_excel(
                writer,
                sheet_name="Inventory",
                index=False
            )

    excel_data = output.getvalue()

    st.download_button(
        label="⬇ Download Excel Report",
        data=excel_data,
        file_name="business_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ==========================================
# PDF REPORT GENERATOR
# ==========================================

def create_pdf():

    pdf_buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Business Intelligence Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            f"Generated On: {datetime.now()}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Executive Summary",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            summary_text,
            styles["BodyText"]
        )
    )

    elements.append(
        PageBreak()
    )

    elements.append(
        Paragraph(
            "KPI Summary",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            f"Revenue: ₹{total_revenue:,.0f}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Units Sold: {total_units:,.0f}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Forecast Demand: {forecast_total:,.0f}",
            styles["BodyText"]
        )
    )

    doc.build(elements)

    pdf_buffer.seek(0)

    return pdf_buffer

# ==========================================
# DOWNLOAD PDF
# ==========================================

if st.button(
    "Generate PDF Report"
):

    pdf_file = create_pdf()

    st.download_button(
        label="⬇ Download PDF Report",
        data=pdf_file,
        file_name="business_report.pdf",
        mime="application/pdf"
    )

st.divider()

# ==========================================
# REPORT STATUS
# ==========================================

st.success(
    "✅ Complete Business Intelligence Reporting Module Ready"
)

st.info(
    """
    Reports Available:

    • Executive Summary Report

    • Forecast Report

    • Inventory Report

    • KPI Report

    • Excel Report

    • PDF Report
    """
)