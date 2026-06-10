import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="EDA Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Exploratory Data Analysis (EDA)")

# ==========================================
# LOAD DATA
# ==========================================

if "eda_data" in st.session_state:
    df = st.session_state["eda_data"].copy()

elif "processed_data" in st.session_state:
    df = st.session_state["processed_data"].copy()

elif "sales_data" in st.session_state:
    df = st.session_state["sales_data"].copy()

else:
    st.warning("⚠ Please upload and preprocess data first.")
    st.stop()
# ==========================================
# COLUMN DETECTION
# ==========================================

product_col = None

if "Medicine_Name" in df.columns:
    product_col = "Medicine_Name"
elif "Product_Name" in df.columns:
    product_col = "Product_Name"

sales_cols = df.select_dtypes(
    include=np.number
).columns.tolist()

numeric_cols = sales_cols

# ==========================================
# OVERVIEW
# ==========================================

st.header("📋 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

with col3:
    st.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

with col4:
    st.metric(
        "Duplicate Rows",
        int(df.duplicated().sum())
    )

st.divider()

# ==========================================
# PREVIEW
# ==========================================

st.subheader("🔍 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

st.divider()

# ==========================================
# SUMMARY
# ==========================================

st.header("📈 Statistical Summary")

if len(numeric_cols) > 0:

    st.dataframe(
        df[numeric_cols].describe(),
        use_container_width=True
    )

st.divider()

# ==========================================
# SALES TREND
# ==========================================

if "Date" in df.columns:

    st.header("📉 Sales Trend Analysis")

    try:

        df["Date"] = pd.to_datetime(df["Date"])

        metric = st.selectbox(
            "Select Metric",
            sales_cols,
            key="trend_metric"
        )

        trend_df = (
            df.groupby("Date")[metric]
            .sum()
            .reset_index()
        )

        st.dataframe(
            trend_df.head(),
            use_container_width=True
        )

        fig = px.line(
            trend_df,
            x="Date",
            y=metric,
            markers=True,
            title=f"{metric} Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:
        st.warning(f"Date Error: {e}")

st.divider()

# ==========================================
# PRODUCT ANALYSIS
# ==========================================

if product_col:

    st.header("💊 Medicine Analysis")

    metric = st.selectbox(
        "Select Metric",
        sales_cols,
        key="medicine_metric"
    )

    product_df = (
        df.groupby(product_col)[metric]
        .sum()
        .reset_index()
        .sort_values(
            metric,
            ascending=False
        )
    )

    st.dataframe(
        product_df,
        use_container_width=True
    )

    fig_product = px.bar(
        product_df,
        x=product_col,
        y=metric,
        title="Medicine Performance"
    )

    st.plotly_chart(
        fig_product,
        use_container_width=True
    )

st.divider()

# ==========================================
# TOP 10 MEDICINES
# ==========================================

if product_col:

    st.header("🏆 Top 10 Medicines")

    top_metric = st.selectbox(
        "Ranking Metric",
        sales_cols,
        key="top_metric"
    )

    top_df = (
        df.groupby(product_col)[top_metric]
        .sum()
        .reset_index()
        .sort_values(
            top_metric,
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_df,
        use_container_width=True
    )

    fig_top = px.bar(
        top_df,
        x=product_col,
        y=top_metric,
        title="Top 10 Medicines"
    )

    st.plotly_chart(
        fig_top,
        use_container_width=True
    )

st.divider()

# ==========================================
# BOTTOM 10 MEDICINES
# ==========================================

if product_col:

    st.header("📉 Bottom 10 Medicines")

    bottom_df = (
        df.groupby(product_col)[top_metric]
        .sum()
        .reset_index()
        .sort_values(
            top_metric,
            ascending=True
        )
        .head(10)
    )

    st.dataframe(
        bottom_df,
        use_container_width=True
    )

    fig_bottom = px.bar(
        bottom_df,
        x=product_col,
        y=top_metric,
        title="Bottom 10 Medicines"
    )

    st.plotly_chart(
        fig_bottom,
        use_container_width=True
    )

st.divider()

# ==========================================
# REGION ANALYSIS
# ==========================================

if "Region" in df.columns:

    st.header("🌍 Region Analysis")

    region_metric = st.selectbox(
        "Region Metric",
        sales_cols,
        key="region_metric"
    )

    region_df = (
        df.groupby("Region")[region_metric]
        .sum()
        .reset_index()
    )

    st.dataframe(
        region_df,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_bar = px.bar(
            region_df,
            x="Region",
            y=region_metric,
            title="Region Performance"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    with col2:

        fig_pie = px.pie(
            region_df,
            names="Region",
            values=region_metric,
            title="Region Contribution"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

st.divider()

# ==========================================
# INVENTORY ANALYSIS
# ==========================================

if "Inventory_Level" in df.columns:

    st.header("📦 Inventory Analysis")

    inventory_df = (
        df.groupby(product_col)["Inventory_Level"]
        .mean()
        .reset_index()
    )

    st.dataframe(
        inventory_df,
        use_container_width=True
    )

    fig_inventory = px.bar(
        inventory_df,
        x=product_col,
        y="Inventory_Level",
        title="Average Inventory by Medicine"
    )

    st.plotly_chart(
        fig_inventory,
        use_container_width=True
    )

st.divider()

# ==========================================
# DISTRIBUTION
# ==========================================

st.header("📊 Distribution Analysis")

selected_col = st.selectbox(
    "Select Numeric Column",
    numeric_cols,
    key="distribution"
)

fig_hist = px.histogram(
    df,
    x=selected_col,
    nbins=30,
    title=f"Distribution of {selected_col}"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

st.divider()

# ==========================================
# CORRELATION
# ==========================================

if len(numeric_cols) > 1:

    st.header("🔥 Correlation Analysis")

    corr = df[numeric_cols].corr()

    st.dataframe(
        corr,
        use_container_width=True
    )

    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )

st.divider()

# ==========================================
# BUSINESS INSIGHTS
# ==========================================

st.header("💡 Business Insights")

if "Revenue" in df.columns:

    st.success(
        f"Total Revenue: ₹{df['Revenue'].sum():,.2f}"
    )

if "Units_Sold" in df.columns:

    st.success(
        f"Total Units Sold: {df['Units_Sold'].sum():,.0f}"
    )

if product_col and "Revenue" in df.columns:

    top_product = (
        df.groupby(product_col)["Revenue"]
        .sum()
        .idxmax()
    )

    st.success(
        f"Best Performing Medicine: {top_product}"
    )

if "Region" in df.columns and "Revenue" in df.columns:

    best_region = (
        df.groupby("Region")["Revenue"]
        .sum()
        .idxmax()
    )

    st.success(
        f"Best Revenue Region: {best_region}"
    )

st.divider()

# ==========================================
# SAVE DATA
# ==========================================

st.session_state["sales_data"] = df.copy()
st.session_state["processed_data"] = df.copy()
st.session_state["eda_data"] = df.copy()

st.success(
    "✅ EDA Completed Successfully. Proceed to Feature Engineering."
)