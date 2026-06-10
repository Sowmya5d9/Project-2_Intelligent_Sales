import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Inventory Optimization",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Optimization & Stock Management")
with st.sidebar:

    st.subheader("Pipeline Status")

    st.write(
        "sales_data:",
        "✅" if "sales_data" in st.session_state else "❌"
    )

    st.write(
        "processed_data:",
        "✅" if "processed_data" in st.session_state else "❌"
    )

    st.write(
        "eda_data:",
        "✅" if "eda_data" in st.session_state else "❌"
    )

    st.write(
        "feature_data:",
        "✅" if "feature_data" in st.session_state else "❌"
    )

    st.write(
        "best_model:",
        "✅" if "best_model" in st.session_state else "❌"
    )

    st.write(
        "forecast_results:",
        "✅" if "forecast_results" in st.session_state else "❌"
    )

# ==========================================
# LOAD DATA
# ==========================================
# ==========================================
# LOAD ORIGINAL CSV DATA
# ==========================================

if "sales_data" not in st.session_state:
    st.error(
        "❌ Please upload dataset first."
    )
    st.stop()

df = st.session_state["sales_data"].copy()

st.success("✅ Using Original Uploaded CSV Data")

# ==========================================
# REQUIRED COLUMNS CHECK
# ==========================================
# ==========================================
# COLUMN MAPPING
# ==========================================

st.header("📌 Column Mapping")

all_columns = df.columns.tolist()

numeric_cols = df.select_dtypes(
    include=np.number
).columns.tolist()

if len(numeric_cols) < 2:

    st.error(
        "Dataset must contain at least 2 numeric columns."
    )

    st.stop()

category_cols = [
    col for col in df.columns
    if df[col].dtype == "object"
]

if len(category_cols) == 0:
    category_cols = all_columns

product_col = st.selectbox(
    "Select Product/Category Column",
    category_cols
)

sales_col = st.selectbox(
    "Select Sales/Demand Column",
    numeric_cols
)

inventory_col = st.selectbox(
    "Select Inventory/Stock Column",
    numeric_cols,
    index=min(1, len(numeric_cols)-1)
)

# ==========================================
# PARAMETERS
# ==========================================

st.header("⚙ Inventory Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    lead_time = st.number_input(
        "Lead Time (Days)",
        min_value=1,
        value=7
    )

with col2:
    service_factor = st.number_input(
        "Service Level Factor",
        min_value=0.1,
        value=1.65
    )

with col3:
    ordering_cost = st.number_input(
        "Ordering Cost (₹)",
        min_value=1,
        value=500
    )

holding_cost = st.number_input(
    "Holding Cost Per Unit (₹)",
    min_value=1,
    value=50
)

st.divider()

# ==========================================
# INVENTORY CALCULATIONS
# ==========================================

st.header("📊 Inventory Analysis")

inventory_df = (
    df.groupby(product_col)
    .agg({
        sales_col: "sum",
        inventory_col: "mean"
    })
    .reset_index()
)
inventory_df.rename(
    columns={
        sales_col: "Units_Sold",
        inventory_col: "Current_Inventory"
    },
    inplace=True
)

# Daily Demand

inventory_df["Daily_Demand"] = (
    inventory_df["Units_Sold"] / 365
)

# Safety Stock

inventory_df["Safety_Stock"] = (
    service_factor *
    inventory_df["Daily_Demand"].std()
)

# Reorder Point

inventory_df["Reorder_Point"] = (
    inventory_df["Daily_Demand"] * lead_time
    + inventory_df["Safety_Stock"]
)

# EOQ

inventory_df["EOQ"] = np.sqrt(
    (
        2 *
        inventory_df["Units_Sold"] *
        ordering_cost
    )
    /
    holding_cost
)

# Inventory Status

conditions = [
    inventory_df["Current_Inventory"]
    < inventory_df["Reorder_Point"],

    inventory_df["Current_Inventory"]
    > inventory_df["EOQ"] * 2
]

choices = [
    "Low Stock",
    "Overstock"
]

inventory_df["Inventory_Status"] = np.select(
    conditions,
    choices,
    default="Optimal"
)

# ==========================================
# KPI METRICS
# ==========================================

st.header("📈 Inventory KPIs")

low_stock = (
    inventory_df[
        inventory_df["Inventory_Status"]
        == "Low Stock"
    ]
    .shape[0]
)

overstock = (
    inventory_df[
        inventory_df["Inventory_Status"]
        == "Overstock"
    ]
    .shape[0]
)

optimal = (
    inventory_df[
        inventory_df["Inventory_Status"]
        == "Optimal"
    ]
    .shape[0]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Low Stock Products",
        low_stock
    )

with col2:
    st.metric(
        "Overstock Products",
        overstock
    )

with col3:
    st.metric(
        "Optimal Products",
        optimal
    )

st.divider()

# ==========================================
# INVENTORY TABLE
# ==========================================

st.header("📋 Inventory Optimization Table")

st.dataframe(
    inventory_df,
    use_container_width=True
)

st.divider()

# ==========================================
# LOW STOCK PRODUCTS
# ==========================================

st.header("⚠ Low Stock Products")

low_stock_df = inventory_df[
    inventory_df["Inventory_Status"]
    == "Low Stock"
]

st.dataframe(
    low_stock_df,
    use_container_width=True
)

# Graph

if not low_stock_df.empty:

    fig_low = px.bar(
        low_stock_df,
        x= product_col,
        y="Current_Inventory",
        color="Inventory_Status",
        title="Low Stock Products"
    )

    st.plotly_chart(
        fig_low,
        use_container_width=True
    )

st.divider()

# ==========================================
# OVERSTOCK PRODUCTS
# ==========================================

st.header("📦 Overstock Products")

overstock_df = inventory_df[
    inventory_df["Inventory_Status"]
    == "Overstock"
]

st.dataframe(
    overstock_df,
    use_container_width=True
)

if not overstock_df.empty:

    fig_over = px.bar(
        overstock_df,
        x= product_col,
        y="Current_Inventory",
        color="Inventory_Status",
        title="Overstock Products"
    )

    st.plotly_chart(
        fig_over,
        use_container_width=True
    )

st.divider()

# ==========================================
# INVENTORY STATUS DISTRIBUTION
# ==========================================

st.header("📊 Inventory Status Distribution")

status_df = (
    inventory_df["Inventory_Status"]
    .value_counts()
    .reset_index()
)

status_df.columns = [
    "Status",
    "Count"
]

col1, col2 = st.columns(2)

with col1:

    fig_bar = px.bar(
        status_df,
        x="Status",
        y="Count",
        title="Inventory Status Count"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

with col2:

    fig_pie = px.pie(
        status_df,
        names="Status",
        values="Count",
        title="Inventory Status Share"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

st.divider()

# ==========================================
# REORDER ANALYSIS
# ==========================================

st.header("🔄 Reorder Point Analysis")

reorder_df = inventory_df[
    [
         product_col,
        "Current_Inventory",
        "Reorder_Point"
    ]
]

st.dataframe(
    reorder_df,
    use_container_width=True
)

fig_reorder = px.bar(
    reorder_df,
    x=product_col,
    y=[
        "Current_Inventory",
        "Reorder_Point"
    ],
    barmode="group",
    title="Inventory vs Reorder Point"
)

st.plotly_chart(
    fig_reorder,
    use_container_width=True
)

st.divider()

# ==========================================
# INVENTORY RECOMMENDATIONS
# ==========================================

st.header("💡 Inventory Recommendations")

recommendations = []

for _, row in inventory_df.iterrows():

    if row["Inventory_Status"] == "Low Stock":

        recommendations.append(
            {
                "Product": row[product_col],
                "Recommendation":
                "Reorder Immediately"
            }
        )

    elif row["Inventory_Status"] == "Overstock":

        recommendations.append(
            {
                "Product": row[product_col],
                "Recommendation":
                "Reduce Inventory"
            }
        )

    else:

        recommendations.append(
            {
                "Product": row[product_col],
                "Recommendation":
                "Maintain Inventory"
            }
        )

recommendation_df = pd.DataFrame(
    recommendations
)

st.dataframe(
    recommendation_df,
    use_container_width=True
)

st.divider()

# ==========================================
# DOWNLOAD REPORT
# ==========================================

st.header("⬇ Download Inventory Report")

csv = inventory_df.to_csv(
    index=False
)

st.download_button(
    label="Download Inventory Report",
    data=csv,
    file_name="inventory_report.csv",
    mime="text/csv"
)

# ==========================================
# SAVE FOR NEXT MODULE
# ==========================================

st.session_state[
    "inventory_results"
] = inventory_df

st.session_state[
    "inventory_recommendations"
] = recommendation_df

st.success(
    "Inventory Optimization Completed Successfully. "
    "Proceed to AI Insights."
)
st.session_state["sales_data"] = df.copy()
st.session_state["processed_data"] = df.copy()
st.session_state["eda_data"] = df.copy()
st.session_state["feature_data"] = df.copy()