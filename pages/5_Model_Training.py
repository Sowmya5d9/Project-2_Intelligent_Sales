import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except:
    XGBOOST_AVAILABLE = False

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Model Training",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Model Training & Evaluation")
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
    st.warning("Please upload and process a dataset first.")
    st.stop()

# ==========================================
# DATA PREVIEW
# ==========================================

st.subheader("Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

# ==========================================
# NUMERIC COLUMNS
# ==========================================

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

if len(numeric_cols) < 2:
    st.error("Need at least two numeric columns.")
    st.stop()

# ==========================================
# TARGET COLUMN
# ==========================================

target_col = st.selectbox(
    "Select Target Column",
    numeric_cols
)

# ==========================================
# FEATURE SELECTION
# ==========================================

feature_cols = st.multiselect(
    "Select Feature Columns",
    [col for col in numeric_cols if col != target_col],
    default=[col for col in numeric_cols if col != target_col][:5]
)

if len(feature_cols) == 0:
    st.warning("Please select at least one feature.")
    st.stop()

# ==========================================
# PREPARE DATA
# ==========================================

model_df = df[feature_cols + [target_col]].copy()

model_df = model_df.fillna(0)

model_df = model_df.dropna(how="all")

if len(model_df) < 10:
    st.error(
        f"Not enough usable rows for training. Rows available: {len(model_df)}"
    )
    st.stop()

X = model_df[feature_cols]
y = model_df[target_col]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

test_size = st.slider(
    "Test Size (%)",
    min_value=10,
    max_value=40,
    value=20
)
if len(X) < 10:
    st.error(
        f"Dataset contains only {len(X)} rows. Need at least 10 rows."
    )
    st.stop()
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=test_size / 100,
    random_state=42
)

st.success(
    f"Training Records: {len(X_train)} | Testing Records: {len(X_test)}"
)

# ==========================================
# TRAIN MODELS
# ==========================================

if st.button("🚀 Train Models"):

    results = []

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
    }

    if XGBOOST_AVAILABLE:
        models["XGBoost"] = XGBRegressor(
            n_estimators=100,
            random_state=42
        )

    best_model = None
    best_score = -999999
    best_name = ""

    progress = st.progress(0)

    for idx, (name, model) in enumerate(models.items()):

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                predictions
            )
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        mape = np.mean(
            np.abs(
                (y_test - predictions)
                /
                np.where(y_test == 0, 1, y_test)
            )
        ) * 100

        results.append({
            "Model": name,
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2 Score": round(r2, 4),
            "MAPE (%)": round(mape, 2)
        })

        if r2 > best_score:
            best_score = r2
            best_model = model
            best_name = name

        progress.progress(
            (idx + 1) / len(models)
        )

    # ==========================================
    # RESULTS DATAFRAME
    # ==========================================

    results_df = pd.DataFrame(results)

    st.session_state["results_df"] = results_df
    st.session_state["best_model"] = best_model
    st.session_state["best_model_name"] = best_name
    st.session_state["feature_columns"] = feature_cols
    st.session_state["target_column"] = target_col
    st.session_state["training_data"] = model_df.copy()

    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    st.subheader("Model Performance")

    st.dataframe(
        results_df,
        use_container_width=True
    )

    # ==========================================
    # BAR CHART
    # ==========================================

    fig = px.bar(
        results_df,
        x="Model",
        y="R2 Score",
        text="R2 Score",
        title="Model Comparison"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================================
    # SAVE MODEL
    # ==========================================

    os.makedirs(
        "models/saved_models",
        exist_ok=True
    )

    model_path = (
        f"models/saved_models/"
        f"{best_name.replace(' ', '_')}.pkl"
    )

    joblib.dump(
        best_model,
        model_path
    )
    st.session_state["model_path"] = model_path

    st.success(
        f"Best Model: {best_name}"
    )

    st.success(
        f"Model Saved: {model_path}"
    )

    # ==========================================
    # PREDICTION PREVIEW
    # ==========================================

    predictions = best_model.predict(X_test)

    preview_df = pd.DataFrame({
        "Actual": y_test.values,
        "Predicted": predictions
    })

    st.subheader("Prediction Preview")

    st.dataframe(
        preview_df.head(20),
        use_container_width=True
    )

    fig2 = px.scatter(
        preview_df,
        x="Actual",
        y="Predicted",
        title="Actual vs Predicted"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================
# SHOW PREVIOUS RESULTS
# ==========================================

if "results_df" in st.session_state:

    st.divider()

    st.subheader("Latest Results")

    st.dataframe(
        st.session_state["results_df"],
        use_container_width=True
    )

# ==========================================
# DOWNLOAD MODEL
# ==========================================

if "best_model_name" in st.session_state:

    model_file = (
        f"models/saved_models/"
        f"{st.session_state['best_model_name'].replace(' ', '_')}.pkl"
    )

    if os.path.exists(model_file):

        with open(model_file, "rb") as file:

            st.download_button(
                label="⬇ Download Trained Model",
                data=file,
                file_name=os.path.basename(model_file),
                mime="application/octet-stream"
            )

# ==========================================
# COMPLETION MESSAGE
# ==========================================

if "best_model" in st.session_state:

    st.success(
        "✅ Model Training Completed Successfully. Proceed to Sales Forecasting."
    )
st.session_state["sales_data"] = df.copy()
st.session_state["processed_data"] = df.copy()
st.session_state["eda_data"] = df.copy()
st.session_state["feature_data"] = df.copy()