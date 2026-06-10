import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from pathlib import Path

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Upload Sales Dataset")
st.markdown("Upload CSV or Excel files for Sales Forecasting and Inventory Optimization.")
# ==========================================
# PIPELINE STATUS
# ==========================================


# ==========================================
# DATABASE FUNCTIONS
# ==========================================

DB_NAME = "database.db"

def save_upload_history(filename):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploaded_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute(
        "INSERT INTO uploaded_data(filename) VALUES(?)",
        (filename,)
    )

    conn.commit()
    conn.close()


def get_upload_history():
    conn = sqlite3.connect(DB_NAME)

    try:
        df = pd.read_sql(
            "SELECT * FROM uploaded_data ORDER BY upload_time DESC",
            conn
        )
    except:
        df = pd.DataFrame()

    conn.close()

    return df


# ==========================================
# FILE UPLOADER
# ==========================================

uploaded_file = st.file_uploader(
    "Choose CSV or Excel File",
    type=["csv", "xlsx", "xls"]
)

# ==========================================
# LOAD DATA
# ==========================================

if uploaded_file is not None:

    try:

        extension = Path(uploaded_file.name).suffix

        if extension == ".csv":
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        save_upload_history(uploaded_file.name)

        st.success("Dataset Uploaded Successfully ✅")

        # Save dataframe in session state
        # Save dataframe in session state
        st.session_state["sales_data"] = df.copy()
        st.session_state["processed_data"] = df.copy()
        st.session_state["eda_data"] = df.copy()
        st.session_state["feature_data"] = df.copy()
        # Backup copy
        st.session_state["master_data"] = df.copy()

        # ==========================================
        # DATASET OVERVIEW
        # ==========================================

        st.header("📊 Dataset Overview")

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
        # DATA PREVIEW
        # ==========================================

        st.subheader("🔍 Dataset Preview")

        st.dataframe(
            df.head(20),
            use_container_width=True
        )

        st.divider()

        # ==========================================
        # COLUMN INFORMATION
        # ==========================================

        st.subheader("📋 Column Information")

        info_df = pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values,
            "Unique Values": [df[col].nunique() for col in df.columns]
        })

        st.dataframe(
            info_df,
            use_container_width=True
        )

        st.divider()

        # ==========================================
        # DESCRIPTIVE STATISTICS
        # ==========================================

        st.subheader("📈 Statistical Summary")

        numeric_df = df.select_dtypes(
            include=["int64", "float64"]
        )

        if not numeric_df.empty:
            st.dataframe(
                numeric_df.describe(),
                use_container_width=True
            )

        st.divider()

        # ==========================================
        # NUMERIC COLUMN DISTRIBUTION
        # ==========================================

        st.subheader("📊 Numeric Data Distribution")

        numeric_columns = numeric_df.columns.tolist()

        if len(numeric_columns) > 0:

            selected_column = st.selectbox(
                "Select Numeric Column",
                numeric_columns
            )

            fig = px.histogram(
                df,
                x=selected_column,
                nbins=30,
                title=f"Distribution of {selected_column}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.divider()

        # ==========================================
        # MISSING VALUES CHART
        # ==========================================

        st.subheader("❗ Missing Values Analysis")

        missing_df = pd.DataFrame({
            "Column": df.columns,
            "Missing Values": df.isnull().sum().values
        })

        st.dataframe(
            missing_df,
            use_container_width=True
        )

        fig_missing = px.bar(
            missing_df,
            x="Column",
            y="Missing Values",
            title="Missing Values by Column"
        )

        st.plotly_chart(
            fig_missing,
            use_container_width=True
        )

        st.divider()

        # ==========================================
        # CATEGORICAL ANALYSIS
        # ==========================================

        st.subheader("📌 Categorical Column Analysis")

        categorical_cols = df.select_dtypes(
            include=["object"]
        ).columns.tolist()

        if len(categorical_cols) > 0:

            cat_col = st.selectbox(
                "Select Categorical Column",
                categorical_cols
            )

            cat_df = (
                df[cat_col]
                .value_counts()
                .reset_index()
            )

            cat_df.columns = [
                cat_col,
                "Count"
            ]

            st.dataframe(
                cat_df,
                use_container_width=True
            )

            fig_cat = px.bar(
                cat_df,
                x=cat_col,
                y="Count",
                title=f"{cat_col} Distribution"
            )

            st.plotly_chart(
                fig_cat,
                use_container_width=True
            )

        st.divider()

        # ==========================================
        # CORRELATION MATRIX
        # ==========================================

        if len(numeric_columns) > 1:

            st.subheader("🔥 Correlation Matrix")

            corr = numeric_df.corr()

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
        # LAST ROWS
        # ==========================================

        st.subheader("📄 Last 10 Rows")

        st.dataframe(
            df.tail(10),
            use_container_width=True
        )

    except Exception as e:

        st.error(f"Error Loading File: {e}")
# ==========================================
# PREVIOUS DATASET PREVIEW
# ==========================================

if (
    uploaded_file is None
    and "sales_data" in st.session_state
):

    st.info("Previously uploaded dataset loaded.")

    st.dataframe(
        st.session_state["sales_data"].head(),
        use_container_width=True
    )

# ==========================================
# UPLOAD HISTORY
# ==========================================

st.header("🗄 Upload History")

history = get_upload_history()

if not history.empty:

    st.dataframe(
        history,
        use_container_width=True
    )

else:
    st.info("No Upload History Found")

# ==========================================
# NAVIGATION MESSAGE
# ==========================================

st.success(
    "Dataset uploaded successfully. Proceed to 'Data Preprocessing' page."
)