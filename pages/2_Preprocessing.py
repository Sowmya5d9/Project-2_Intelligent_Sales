import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Data Preprocessing",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 Data Preprocessing")

# ==========================================
# CHECK DATASET
# ==========================================

if "processed_data" in st.session_state:
    df = st.session_state["processed_data"].copy()

elif "sales_data" in st.session_state:
    df = st.session_state["sales_data"].copy()

else:
    st.warning("⚠ Please upload a dataset first from Upload Data page.")
    st.stop()

st.success("Dataset Loaded Successfully")

# ==========================================
# DATASET SUMMARY
# ==========================================

st.header("📊 Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

with col3:
    st.metric("Missing Values", int(df.isnull().sum().sum()))

with col4:
    st.metric("Duplicates", int(df.duplicated().sum()))

st.divider()

# ==========================================
# ORIGINAL DATA
# ==========================================

st.subheader("📋 Original Dataset")

st.dataframe(df.head(20), use_container_width=True)

st.divider()

# ==========================================
# MISSING VALUE ANALYSIS
# ==========================================

st.header("❗ Missing Value Analysis")

missing_df = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values,
    "Percentage": (
        df.isnull().sum().values / len(df) * 100
    ).round(2)
})

st.dataframe(missing_df, use_container_width=True)

fig_missing = px.bar(
    missing_df,
    x="Column",
    y="Missing Values",
    title="Missing Values by Column"
)

st.plotly_chart(fig_missing, use_container_width=True)

st.divider()

# ==========================================
# HANDLE MISSING VALUES
# ==========================================

st.header("🛠 Missing Value Treatment")

missing_option = st.selectbox(
    "Choose Missing Value Handling Method",
    [
        "Do Nothing",
        "Fill Numeric with Mean",
        "Fill Numeric with Median",
        "Drop Rows with Missing Values"
    ]
)

processed_df = df.copy()

if st.button("Apply Missing Value Treatment"):

    if missing_option == "Fill Numeric with Mean":

        numeric_cols = processed_df.select_dtypes(
            include=np.number
        ).columns

        for col in numeric_cols:
            processed_df[col] = processed_df[col].fillna(
                processed_df[col].mean()
            )

    elif missing_option == "Fill Numeric with Median":

        numeric_cols = processed_df.select_dtypes(
            include=np.number
        ).columns

        for col in numeric_cols:
            processed_df[col] = processed_df[col].fillna(
                processed_df[col].median()
            )

    elif missing_option == "Drop Rows with Missing Values":

        processed_df.dropna(inplace=True)

    st.session_state["processed_data"] = processed_df.copy()
    st.session_state["sales_data"] = processed_df.copy()

    st.success("Missing Values Processed Successfully")

st.divider()

# ==========================================
# DUPLICATE ANALYSIS
# ==========================================

st.header("📑 Duplicate Records")

duplicate_count = df.duplicated().sum()

dup_df = pd.DataFrame({
    "Metric": ["Total Duplicate Records"],
    "Value": [duplicate_count]
})

st.dataframe(dup_df, use_container_width=True)

fig_dup = px.bar(
    dup_df,
    x="Metric",
    y="Value",
    title="Duplicate Records"
)

st.plotly_chart(fig_dup, use_container_width=True)

st.divider()

# ==========================================
# REMOVE DUPLICATES
# ==========================================

st.header("🗑 Remove Duplicates")

if st.button("Remove Duplicate Records"):

    before = len(processed_df)

    processed_df = processed_df.drop_duplicates()

    after = len(processed_df)

    st.session_state["processed_data"] = processed_df.copy()
    st.session_state["sales_data"] = processed_df.copy()

    st.success(
        f"{before - after} Duplicate Rows Removed Successfully"
    )

st.divider()

# ==========================================
# OUTLIER ANALYSIS
# ==========================================

st.header("🚨 Outlier Detection")

numeric_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

if len(numeric_columns) > 0:

    selected_col = st.selectbox(
        "Select Numeric Column",
        numeric_columns
    )

    st.subheader("Box Plot")

    fig_box = px.box(
        df,
        y=selected_col,
        title=f"Outlier Detection - {selected_col}"
    )

    st.plotly_chart(
        fig_box,
        use_container_width=True
    )

    q1 = df[selected_col].quantile(0.25)
    q3 = df[selected_col].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[
        (df[selected_col] < lower_bound)
        | (df[selected_col] > upper_bound)
    ]

    st.subheader("Detected Outliers")

    st.dataframe(
        outliers,
        use_container_width=True
    )

    st.write("Total Outliers:", len(outliers))

st.divider()

# ==========================================
# REMOVE OUTLIERS
# ==========================================

st.header("✂ Remove Outliers")

if len(numeric_columns) > 0:

    outlier_column = st.selectbox(
        "Select Column for Outlier Removal",
        numeric_columns,
        key="outlier_remove"
    )

    if st.button("Remove Outliers"):

        q1 = processed_df[outlier_column].quantile(0.25)
        q3 = processed_df[outlier_column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        before_rows = len(processed_df)

        processed_df = processed_df[
            (processed_df[outlier_column] >= lower)
            &
            (processed_df[outlier_column] <= upper)
        ]

        after_rows = len(processed_df)

        st.session_state["processed_data"] = processed_df.copy()
        st.session_state["sales_data"] = processed_df.copy()

        st.success(
            f"{before_rows - after_rows} Outliers Removed Successfully"
        )

st.divider()

# ==========================================
# BEFORE VS AFTER COMPARISON
# ==========================================

st.header("📈 Before vs After Comparison")

processed_df = st.session_state.get(
    "processed_data",
    df.copy()
)

comparison_df = pd.DataFrame({
    "Metric": [
        "Rows",
        "Columns",
        "Missing Values",
        "Duplicates"
    ],
    "Original": [
        df.shape[0],
        df.shape[1],
        df.isnull().sum().sum(),
        df.duplicated().sum()
    ],
    "Processed": [
        processed_df.shape[0],
        processed_df.shape[1],
        processed_df.isnull().sum().sum(),
        processed_df.duplicated().sum()
    ]
})

st.dataframe(
    comparison_df,
    use_container_width=True
)

fig_compare = px.bar(
    comparison_df,
    x="Metric",
    y=["Original", "Processed"],
    barmode="group",
    title="Before vs After Preprocessing"
)

st.plotly_chart(
    fig_compare,
    use_container_width=True
)

st.divider()

# ==========================================
# CLEANED DATASET
# ==========================================

st.header("✅ Cleaned Dataset")

st.dataframe(
    processed_df.head(20),
    use_container_width=True
)

st.divider()

# ==========================================
# SAVE CLEANED DATA
# ==========================================

if st.button("💾 Save Cleaned Dataset"):

    st.session_state["processed_data"] = processed_df.copy()
    st.session_state["sales_data"] = processed_df.copy()
    st.session_state["eda_data"] = processed_df.copy()

    st.success(
        "Processed Dataset Saved Successfully"
    )

# ==========================================
# DOWNLOAD CLEANED DATA
# ==========================================

csv = processed_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Cleaned Dataset",
    data=csv,
    file_name="cleaned_sales_data.csv",
    mime="text/csv"
)
st.session_state["processed_data"] = processed_df.copy()
st.session_state["sales_data"] = processed_df.copy()
st.session_state["eda_data"] = processed_df.copy()
st.success(
    "Preprocessing Completed. Proceed to EDA Analysis Page."
)