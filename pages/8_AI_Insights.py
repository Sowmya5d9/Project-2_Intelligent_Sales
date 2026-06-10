import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Insights",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI-Powered Business Insights")

# ==========================================
# LOAD DATA
# ==========================================

if "feature_data" not in st.session_state:
    st.warning("⚠ Please complete previous modules first.")
    st.stop()

df = st.session_state["feature_data"].copy()

forecast_df = st.session_state.get(
    "forecast_results",
    pd.DataFrame()
)

inventory_df = st.session_state.get(
    "inventory_results",
    pd.DataFrame()
)

# ==========================================
# KPI DASHBOARD
# ==========================================

st.header("📊 Executive KPI Dashboard")

col1, col2, col3, col4 = st.columns(4)

# Revenue
total_revenue = (
    df["Revenue"].sum()
    if "Revenue" in df.columns
    else 0
)

# Units Sold
total_units = (
    df["Units_Sold"].sum()
    if "Units_Sold" in df.columns
    else 0
)

# Forecast
forecast_total = (
    forecast_df["Forecasted_Sales"].sum()
    if not forecast_df.empty
    else 0
)

# Products
if "Product_Name" in df.columns:
    total_products = df["Product_Name"].nunique()

elif "Medicine_Name" in df.columns:
    total_products = df["Medicine_Name"].nunique()

else:
    total_products = 0

with col1:
    st.metric(
        "Total Revenue",
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
# SALES INSIGHTS
# ==========================================

st.header("📈 Sales Insights")

sales_insights = []

if "Revenue" in df.columns:

    avg_revenue = df["Revenue"].mean()

    sales_insights.append(
        f"Average Revenue per Record: ₹{avg_revenue:,.2f}"
    )

    sales_insights.append(
        f"Total Revenue Generated: ₹{total_revenue:,.0f}"
    )

if "Units_Sold" in df.columns:

    avg_units = df["Units_Sold"].mean()

    sales_insights.append(
        f"Average Units Sold: {avg_units:.2f}"
    )

for item in sales_insights:
    st.success(item)

st.divider()

# ==========================================
# FORECAST INSIGHTS
# ==========================================

st.header("🔮 Forecast Insights")

if not forecast_df.empty:

    avg_forecast = forecast_df[
        "Forecasted_Sales"
    ].mean()

    max_forecast = forecast_df[
        "Forecasted_Sales"
    ].max()

    min_forecast = forecast_df[
        "Forecasted_Sales"
    ].min()

    st.success(
        f"Expected Average Demand: {avg_forecast:.2f}"
    )

    st.success(
        f"Peak Demand Forecast: {max_forecast:.2f}"
    )

    st.success(
        f"Lowest Forecast Demand: {min_forecast:.2f}"
    )

    fig_forecast = px.line(
        forecast_df,
        x="Date",
        y="Forecasted_Sales",
        markers=True,
        title="Forecast Demand Trend"
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

else:
    st.info(
        "Run Sales Forecasting module first."
    )

st.divider()

# ==========================================
# INVENTORY INSIGHTS
# ==========================================

st.header("📦 Inventory Insights")

if not inventory_df.empty:

    low_stock = inventory_df[
        inventory_df["Inventory_Status"]
        == "Low Stock"
    ].shape[0]

    overstock = inventory_df[
        inventory_df["Inventory_Status"]
        == "Overstock"
    ].shape[0]

    optimal = inventory_df[
        inventory_df["Inventory_Status"]
        == "Optimal"
    ].shape[0]

    st.warning(
        f"Low Stock Products: {low_stock}"
    )

    st.warning(
        f"Overstock Products: {overstock}"
    )

    st.success(
        f"Optimal Products: {optimal}"
    )

    status_df = (
        inventory_df["Inventory_Status"]
        .value_counts()
        .reset_index()
    )

    status_df.columns = [
        "Status",
        "Count"
    ]

    fig_status = px.pie(
        status_df,
        names="Status",
        values="Count",
        title="Inventory Status Distribution"
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )

else:
    st.info(
        "Run Inventory Optimization module first."
    )

st.divider()

# ==========================================
# PRODUCT PERFORMANCE
# ==========================================

st.header("🏆 Product Performance Insights")

product_col = None

if "Product_Name" in df.columns:
    product_col = "Product_Name"

elif "Medicine_Name" in df.columns:
    product_col = "Medicine_Name"

if (
    product_col is not None
    and "Revenue" in df.columns
):

    product_df = (
        df.groupby(product_col)["Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    top_products = product_df.head(10)

    st.dataframe(
        top_products,
        use_container_width=True
    )

    fig_products = px.bar(
        top_products,
        x=product_col,
        y="Revenue",
        title="Top 10 Products"
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

st.divider()

# ==========================================
# REGION INSIGHTS
# ==========================================

st.header("🌍 Regional Performance")

if (
    "Region" in df.columns
    and "Revenue" in df.columns
):

    region_df = (
        df.groupby("Region")["Revenue"]
        .sum()
        .reset_index()
    )

    st.dataframe(
        region_df,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_region = px.bar(
            region_df,
            x="Region",
            y="Revenue",
            title="Revenue by Region"
        )

        st.plotly_chart(
            fig_region,
            use_container_width=True
        )

    with col2:

        fig_region_pie = px.pie(
            region_df,
            names="Region",
            values="Revenue",
            title="Regional Contribution"
        )

        st.plotly_chart(
            fig_region_pie,
            use_container_width=True
        )

st.divider()

# ==========================================
# AI RECOMMENDATIONS
# ==========================================

st.header("🤖 AI Recommendations")

recommendations = []

# Revenue Recommendations

if "Revenue" in df.columns:

    if total_revenue > 1000000:
        recommendations.append(
            "Revenue performance is strong. Maintain current growth strategy."
        )
    else:
        recommendations.append(
            "Revenue can be improved through targeted promotions."
        )

# Forecast Recommendations

if not forecast_df.empty:

    if forecast_total > total_units:
        recommendations.append(
            "Demand expected to increase. Increase inventory planning."
        )
    else:
        recommendations.append(
            "Demand stable. Maintain current inventory strategy."
        )

# Inventory Recommendations

if not inventory_df.empty:

    if low_stock > 0:
        recommendations.append(
            f"Reorder stock for {low_stock} products immediately."
        )

    if overstock > 0:
        recommendations.append(
            f"Reduce stock levels for {overstock} overstocked products."
        )

recommendation_df = pd.DataFrame({
    "AI Recommendation": recommendations
})

st.dataframe(
    recommendation_df,
    use_container_width=True
)

st.divider()

# ==========================================
# EXECUTIVE SUMMARY
# ==========================================

st.header("📄 Executive Summary")

summary_text = f"""
Total Revenue Generated: ₹{total_revenue:,.0f}

Total Units Sold: {total_units:,.0f}

Forecast Demand: {forecast_total:,.0f}

Total Products Managed: {total_products}

The business demonstrates measurable sales activity and inventory performance.

The forecasting model predicts future demand trends and helps optimize stock planning.

Inventory optimization highlights low-stock and overstock situations, enabling proactive decision-making.

Recommendations generated above can improve supply chain efficiency, reduce inventory costs, and support revenue growth.
"""

st.text_area(
    "Business Summary",
    summary_text,
    height=300
)

# ==========================================
# SAVE FOR REPORTS
# ==========================================

st.session_state["executive_summary"] = summary_text

st.success(
    "AI Insights Generated Successfully. Proceed to Reports Module."
)