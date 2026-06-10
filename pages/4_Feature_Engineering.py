import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Feature Engineering",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Feature Engineering")
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

# ==========================================
# LOAD DATA
# ==========================================

if "feature_data" in st.session_state:
    df = st.session_state["feature_data"].copy()

elif "eda_data" in st.session_state:
    df = st.session_state["eda_data"].copy()

elif "processed_data" in st.session_state:
    df = st.session_state["processed_data"].copy()

elif "sales_data" in st.session_state:
    df = st.session_state["sales_data"].copy()

else:
    st.warning("⚠️ Please upload and process a dataset first.")
    st.stop()

st.success("Dataset Loaded Successfully")

# ==========================================
# DATASET PREVIEW
# ==========================================

st.header("📋 Current Dataset")

st.dataframe(df.head(10), use_container_width=True)

st.divider()

# ==========================================
# DATE COLUMN DETECTION
# ==========================================

date_columns = []

for col in df.columns:
    try:
        pd.to_datetime(df[col])
        date_columns.append(col)
    except:
        pass

if len(date_columns) == 0:
    st.warning("⚠️ No Date Column Found.")
else:

    date_col = st.selectbox(
        "Select Date Column",
        date_columns
    )

    df[date_col] = pd.to_datetime(df[date_col])

    # ==========================================
    # BASIC DATE FEATURES
    # ==========================================

    st.header("📅 Date Feature Engineering")

    if st.button("Generate Date Features"):

        df["Year"] = df[date_col].dt.year
        df["Month"] = df[date_col].dt.month
        df["Month_Name"] = df[date_col].dt.month_name()
        df["Quarter"] = df[date_col].dt.quarter
        df["Week"] = df[date_col].dt.isocalendar().week
        df["Day"] = df[date_col].dt.day
        df["Day_Of_Week"] = df[date_col].dt.dayofweek
        df["Weekend"] = np.where(
            df["Day_Of_Week"] >= 5,
            1,
            0
        )

        st.success("Date Features Generated Successfully")

        st.session_state["feature_data"] = df.copy()
        st.session_state["eda_data"] = df.copy()

# ==========================================
# LOAD UPDATED DATA
# ==========================================

df = st.session_state.get(
    "feature_data",
    df
)

# ==========================================
# FEATURE PREVIEW
# ==========================================

st.header("📊 Engineered Features Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

st.divider()

# ==========================================
# LAG FEATURES
# ==========================================

st.header("⏳ Lag Feature Generation")

numeric_cols = df.select_dtypes(
    include=np.number
).columns.tolist()

if len(numeric_cols) > 0:

    lag_column = st.selectbox(
        "Select Column for Lag Feature",
        numeric_cols
    )

    lag_period = st.slider(
        "Lag Period",
        1,
        30,
        1
    )

    if st.button("Generate Lag Feature"):

        df[f"{lag_column}_Lag_{lag_period}"] = (
            df[lag_column].shift(lag_period)
        )

        st.session_state["feature_data"] = df.copy()
        st.session_state["eda_data"] = df.copy()

        st.success(
            f"Lag Feature Created: {lag_column}_Lag_{lag_period}"
        )

st.divider()

# ==========================================
# ROLLING MEAN
# ==========================================

st.header("📈 Rolling Mean Feature")

if len(numeric_cols) > 0:

    rolling_col = st.selectbox(
        "Select Column",
        numeric_cols,
        key="rolling"
    )

    rolling_window = st.slider(
        "Rolling Window",
        2,
        30,
        7
    )

    if st.button("Generate Rolling Mean"):

        df[f"{rolling_col}_RollingMean"] = (
            df[rolling_col]
            .rolling(rolling_window)
            .mean()
        )

        st.session_state["feature_data"] = df.copy()
        st.session_state["eda_data"] = df.copy()

        st.success(
            f"Rolling Mean Feature Generated"
        )

st.divider()

# ==========================================
# MOVING AVERAGE
# ==========================================

st.header("📉 Moving Average Feature")

if len(numeric_cols) > 0:

    ma_col = st.selectbox(
        "Select Column",
        numeric_cols,
        key="moving_average"
    )

    ma_window = st.slider(
        "Moving Average Window",
        2,
        30,
        5
    )

    if st.button("Generate Moving Average"):

        df[f"{ma_col}_MovingAvg"] = (
            df[ma_col]
            .rolling(ma_window)
            .mean()
        )

        st.session_state["feature_data"] = df.copy()
        st.session_state["eda_data"] = df.copy()

        st.success(
            "Moving Average Generated"
        )

st.divider()

# ==========================================
# FEATURE SUMMARY
# ==========================================

df = st.session_state.get(
    "feature_data",
    df
)

st.header("📋 Feature Summary")

feature_info = pd.DataFrame({
    "Feature": df.columns,
    "Data Type": df.dtypes.astype(str)
})

st.dataframe(
    feature_info,
    use_container_width=True
)

st.divider()

# ==========================================
# NUMERIC FEATURE DISTRIBUTION
# ==========================================

st.header("📊 Feature Distribution")

updated_numeric = df.select_dtypes(
    include=np.number
).columns.tolist()

if len(updated_numeric) > 0:

    feature_col = st.selectbox(
        "Select Feature",
        updated_numeric,
        key="feature_distribution"
    )

    fig = px.histogram(
        df,
        x=feature_col,
        nbins=30,
        title=f"Distribution of {feature_col}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================
# CORRELATION ANALYSIS
# ==========================================

st.header("🔥 Feature Correlation")

corr_df = df.select_dtypes(
    include=np.number
)

if corr_df.shape[1] > 1:

    corr_matrix = corr_df.corr()

    st.dataframe(
        corr_matrix,
        use_container_width=True
    )

    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Feature Correlation Heatmap"
    )

    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )

st.divider()

# ==========================================
# MONTHLY SALES ANALYSIS
# ==========================================

if "Month" in df.columns:

    st.header("📅 Monthly Analysis")

    sales_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    selected_metric = st.selectbox(
        "Select Monthly Metric",
        sales_cols,
        key="monthly_metric"
    )

    monthly_df = (
        df.groupby("Month")[selected_metric]
        .sum()
        .reset_index()
    )

    st.dataframe(
        monthly_df,
        use_container_width=True
    )

    fig_month = px.line(
        monthly_df,
        x="Month",
        y=selected_metric,
        markers=True,
        title="Monthly Trend"
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

st.divider()

# ==========================================
# FINAL ENGINEERED DATASET
# ==========================================

st.header("✅ Final Engineered Dataset")

st.dataframe(
    df.head(20),
    use_container_width=True
)

st.divider()

# ==========================================
# DOWNLOAD DATASET
# ==========================================

csv = df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Engineered Dataset",
    data=csv,
    file_name="engineered_dataset.csv",
    mime="text/csv"
)

# ==========================================
# SAVE FOR NEXT MODULE
# ==========================================

st.session_state["sales_data"] = df.copy()
st.session_state["processed_data"] = df.copy()
st.session_state["eda_data"] = df.copy()
st.session_state["feature_data"] = df.copy()

st.success(
    "Feature Engineering Completed Successfully. Proceed to Model Training."
)