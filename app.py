import streamlit as st
from datetime import datetime

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Intelligent Sales Forecasting",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
.main-title {
    font-size: 40px;
    font-weight: bold;
    color: #1E88E5;
}

.sub-title {
    font-size: 20px;
    color: #555555;
}

.metric-card {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #dddddd;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown(
    '<p class="main-title">📈 Intelligent Sales Forecasting & Inventory Optimization System</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">AI-Powered Sales Prediction, Inventory Optimization & Business Intelligence Dashboard</p>',
    unsafe_allow_html=True
)

st.divider()

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135673.png",
        width=120
    )

    st.title("Navigation")

    st.success("Use the Pages menu above to navigate.")

    st.markdown("---")

    st.write("### Available Modules")

    st.markdown("""
    ✅ Upload Dataset

    ✅ Data Preprocessing

    ✅ EDA Analysis

    ✅ Feature Engineering

    ✅ Model Training

    ✅ Sales Forecasting

    ✅ Inventory Optimization

    ✅ AI Insights

    ✅ Reports
    """)

    st.markdown("---")
    st.caption(f"Today: {datetime.now().strftime('%d-%m-%Y')}")

# -------------------------------
# DASHBOARD OVERVIEW
# -------------------------------
st.subheader("📊 Project Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Forecast Accuracy",
        value="92%"
    )

with col2:
    st.metric(
        label="Products Tracked",
        value="100"
    )

with col3:
    st.metric(
        label="Inventory Health",
        value="95%"
    )

with col4:
    st.metric(
        label="Active Models",
        value="4"
    )

st.divider()

# -------------------------------
# PROJECT DESCRIPTION
# -------------------------------
st.subheader("🎯 Project Objective")

st.info("""
Inaccurate sales forecasts often lead to stockouts, lost sales,
overstocking, and increased inventory costs.

This Intelligent Sales Forecasting System uses Machine Learning,
Time Series Forecasting, Inventory Analytics, and Business Intelligence
techniques to predict future demand and optimize inventory decisions.
""")

# -------------------------------
# FEATURES SECTION
# -------------------------------
st.subheader("🚀 Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
### 📂 Data Management

- Upload CSV Files
- Upload Excel Files
- Data Validation
- Data Cleaning
- Data Storage
""")

    st.markdown("""
### 🧹 Data Preprocessing

- Missing Value Handling
- Duplicate Removal
- Outlier Detection
- Feature Scaling
- Encoding
""")

with col2:
    st.markdown("""
### 🤖 Machine Learning

- Linear Regression
- Random Forest
- XGBoost
- Prophet Forecasting
""")

    st.markdown("""
### 📈 Business Intelligence

- Sales Trends
- Product Analysis
- Inventory Optimization
- AI Insights
- PDF Reports
""")

st.divider()

# -------------------------------
# WORKFLOW
# -------------------------------
st.subheader("⚙️ Project Workflow")

st.markdown("""
1️⃣ Upload Dataset

⬇️

2️⃣ Data Preprocessing

⬇️

3️⃣ Exploratory Data Analysis (EDA)

⬇️

4️⃣ Feature Engineering

⬇️

5️⃣ Model Training

⬇️

6️⃣ Sales Forecasting

⬇️

7️⃣ Inventory Optimization

⬇️

8️⃣ AI Insights

⬇️

9️⃣ Report Generation
""")

st.divider()

# -------------------------------
# EXPECTED OUTPUTS
# -------------------------------
st.subheader("📋 Expected Outputs")

st.markdown("""
✔ Future Sales Forecasts

✔ Inventory Recommendations

✔ Reorder Point Calculation

✔ Safety Stock Calculation

✔ Business Insights

✔ Forecast Accuracy Reports

✔ PDF & Excel Reports

✔ Interactive Dashboards
""")

# -------------------------------
# FOOTER
# -------------------------------
st.divider()

st.caption(
    "Developed using Streamlit, Machine Learning, Time Series Forecasting, and Business Intelligence."
)