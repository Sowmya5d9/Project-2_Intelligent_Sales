import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import timedelta

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Sales Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales Forecasting")
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

# ==========================================
# CHECK MODEL
# ==========================================

if "best_model" not in st.session_state:
    st.error(
        "❌ No trained model found. Train a model first."
    )
    st.stop()

if "feature_data" in st.session_state:
    df = st.session_state["feature_data"].copy()

elif "eda_data" in st.session_state:
    df = st.session_state["eda_data"].copy()

elif "processed_data" in st.session_state:
    df = st.session_state["processed_data"].copy()

elif "sales_data" in st.session_state:
    df = st.session_state["sales_data"].copy()

else:
    st.error(
        "❌ Dataset not found. Upload dataset first."
    )
    st.stop()

# ==========================================
# LOAD DATA
# ==========================================

model = st.session_state["best_model"]

feature_cols = st.session_state.get(
    "feature_columns",
    []
)

target_col = st.session_state.get(
    "target_column",
    None
)

if len(feature_cols) == 0:
    st.error(
        "❌ Feature columns not found. Retrain model."
    )
    st.stop()
# ==========================================
# DATA PREVIEW
# ==========================================

st.header("📋 Dataset Used For Forecasting")

st.dataframe(
    df.head(10),
    use_container_width=True
)

st.divider()

# ==========================================
# FORECAST OPTIONS
# ==========================================

st.header("⚙ Forecast Settings")

forecast_days = st.selectbox(
    "Forecast Period",
    [
        7,
        30,
        90,
        180,
        365
    ]
)

# ==========================================
# CREATE FUTURE DATA
# ==========================================

st.header("🔮 Generate Forecast")

if st.button("Generate Forecast"):

    try:

        latest_row = df.iloc[-1]

        future_records = []

        # ----------------------------------
        # DATE COLUMN
        # ----------------------------------

        if "Date" in df.columns:

            last_date = pd.to_datetime(
                df["Date"]
            ).max()

        else:

            last_date = pd.Timestamp.today()

        # ----------------------------------
        # FUTURE DATA CREATION
        # ----------------------------------

        for i in range(1, forecast_days + 1):

            future_date = last_date + timedelta(days=i)

            record = {}

            for col in feature_cols:

                if col in df.columns:

                    if pd.api.types.is_numeric_dtype(
                        df[col]
                    ):

                        record[col] = df[col].mean()

                    else:
                        record[col] = 0

                else:
                    record[col] = 0

            future_records.append(record)

        future_df = pd.DataFrame(
            future_records
        )

        # ----------------------------------
        # PREDICTIONS
        # ----------------------------------

        predictions = model.predict(
            future_df
        )

        forecast_df = pd.DataFrame({
            "Date": [
                last_date + timedelta(days=i)
                for i in range(
                    1,
                    forecast_days + 1
                )
            ],
            "Forecasted_Sales": predictions
        })

        # Remove negative forecasts

        forecast_df[
            "Forecasted_Sales"
        ] = forecast_df[
            "Forecasted_Sales"
        ].clip(lower=0)

        # Save for reports page

        st.session_state[
            "forecast_results"
        ] = forecast_df

        # ==================================
        # FORECAST TABLE
        # ==================================

        st.header("📋 Forecast Results")

        st.dataframe(
            forecast_df,
            use_container_width=True
        )

        # ==================================
        # FORECAST SUMMARY
        # ==================================

        st.header("📊 Forecast Summary")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Forecast",
                round(
                    forecast_df[
                        "Forecasted_Sales"
                    ].sum(),
                    2
                )
            )

        with col2:

            st.metric(
                "Average Forecast",
                round(
                    forecast_df[
                        "Forecasted_Sales"
                    ].mean(),
                    2
                )
            )

        with col3:

            st.metric(
                "Maximum Forecast",
                round(
                    forecast_df[
                        "Forecasted_Sales"
                    ].max(),
                    2
                )
            )

        # ==================================
        # FORECAST TREND GRAPH
        # ==================================

        st.header("📈 Forecast Trend")

        fig = px.line(
            forecast_df,
            x="Date",
            y="Forecasted_Sales",
            markers=True,
            title="Future Sales Forecast"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ==================================
        # BAR CHART
        # ==================================

        st.header("📊 Forecast Distribution")

        fig_bar = px.bar(
            forecast_df,
            x="Date",
            y="Forecasted_Sales",
            title="Forecast Sales Distribution"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

        # ==================================
        # HISTORICAL VS FORECAST
        # ==================================

        if target_col in df.columns:

            st.header(
                "📉 Historical vs Forecast"
            )

            history_df = pd.DataFrame({
                "Date": pd.date_range(
                    end=last_date,
                    periods=min(
                        len(df),
                        50
                    )
                ),
                "Actual": df[
                    target_col
                ].tail(50).values
            })

            fig_compare = px.line(
                history_df,
                x="Date",
                y="Actual",
                title="Recent Historical Sales"
            )

            st.plotly_chart(
                fig_compare,
                use_container_width=True
            )

        # ==================================
        # FORECAST INSIGHTS
        # ==================================

        st.header("💡 Business Insights")

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
            f"Average Expected Demand: "
            f"{avg_forecast:.2f}"
        )

        st.success(
            f"Peak Demand Forecast: "
            f"{max_forecast:.2f}"
        )

        st.success(
            f"Lowest Demand Forecast: "
            f"{min_forecast:.2f}"
        )

        if max_forecast > avg_forecast * 1.20:

            st.warning(
                "Potential demand spike detected."
            )

        if min_forecast < avg_forecast * 0.80:

            st.warning(
                "Potential demand slowdown detected."
            )

        # ==================================
        # DOWNLOAD CSV
        # ==================================

        st.header("⬇ Download Forecast")

        csv = forecast_df.to_csv(
            index=False
        )

        st.download_button(
            label="Download Forecast CSV",
            data=csv,
            file_name="forecast_results.csv",
            mime="text/csv"
        )

        st.success(
            "Forecast Generated Successfully."
        )

    except Exception as e:

        st.error(
            f"Forecast Error: {str(e)}"
        )

# ==========================================
# PREVIOUS FORECASTS
# ==========================================

if "forecast_results" in st.session_state:

    st.divider()

    st.header(
        "📄 Latest Forecast Results"
    )

    st.dataframe(
        st.session_state[
            "forecast_results"
        ].head(20),
        use_container_width=True
    )

# ==========================================
# COMPLETION MESSAGE
# ==========================================

st.success(
    "Sales Forecasting Completed. "
    "Proceed to Inventory Optimization."
)
st.session_state["sales_data"] = df.copy()
st.session_state["processed_data"] = df.copy()
st.session_state["eda_data"] = df.copy()
st.session_state["feature_data"] = df.copy()