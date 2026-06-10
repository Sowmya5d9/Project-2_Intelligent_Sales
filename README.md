# 📊 AI-Powered Business Intelligence & Inventory Optimization System

## 🚀 Project Overview

The AI-Powered Business Intelligence & Inventory Optimization System is a Streamlit-based web application that helps businesses analyze sales data, forecast future demand, optimize inventory levels, and generate intelligent business insights.

The system supports multiple types of datasets and allows users to perform end-to-end business analytics through an interactive dashboard.

---

## ✨ Features

### 1. Data Upload

* Upload CSV datasets.
* Automatic dataset preview.
* Supports various business datasets.

### 2. Data Preprocessing

* Handle missing values.
* Remove duplicates.
* Data cleaning and preparation.

### 3. Exploratory Data Analysis (EDA)

* Statistical summary.
* Distribution analysis.
* Correlation analysis.
* Interactive visualizations.

### 4. Feature Engineering

* Generate machine learning features.
* Prepare data for model training.
* Numerical feature extraction.

### 5. Model Training & Evaluation

Supported Models:

* Linear Regression
* Random Forest Regressor
* XGBoost Regressor (Optional)

Evaluation Metrics:

* MAE
* RMSE
* R² Score
* MAPE

The best-performing model is automatically selected and saved.

### 6. Sales Forecasting

* Forecast future sales demand.
* Multiple forecast periods:

  * 7 Days
  * 30 Days
  * 90 Days
  * 180 Days
  * 365 Days
* Forecast visualization and reports.

### 7. Inventory Optimization

* Dynamic column mapping.
* Works with different dataset structures.
* Safety Stock Calculation.
* Reorder Point Analysis.
* Economic Order Quantity (EOQ).
* Inventory Status Classification:

  * Low Stock
  * Overstock
  * Optimal

### 8. AI-Powered Insights

* Revenue Analysis.
* Demand Forecast Insights.
* Inventory Performance Analysis.
* Product Performance Analysis.
* Regional Performance Analysis.
* Automated Business Recommendations.

### 9. Report Generation

Generate:

* Forecast Reports
* Inventory Reports
* Executive Summary
* Excel Reports
* PDF Reports

---

## 🛠 Technologies Used

### Frontend

* Streamlit

### Data Processing

* Pandas
* NumPy

### Visualization

* Plotly Express

### Machine Learning

* Scikit-learn
* XGBoost

### Model Storage

* Joblib

### Reporting

* ReportLab
* XlsxWriter

---

## 📂 Project Structure

```text
Business_Intelligence_Project/
│
├── app.py
├── pages/
│   ├── 1_Data_Upload.py
│   ├── 2_Data_Preprocessing.py
│   ├── 3_EDA.py
│   ├── 4_Feature_Engineering.py
│   ├── 5_Model_Training.py
│   ├── 6_Sales_Forecasting.py
│   ├── 7_Inventory_Optimization.py
│   ├── 8_AI_Insights.py
│   └── 9_Reports.py
│
├── models/
│   └── saved_models/
│
├── requirements.txt
└── README.md
```

---

## ⚙ Installation

### Clone Repository

```bash
git clone <repository-url>
cd Business_Intelligence_Project
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶ Run Application

```bash
streamlit run app.py
```

---

## 📈 Workflow

1. Upload Dataset
2. Data Preprocessing
3. EDA
4. Feature Engineering
5. Model Training
6. Sales Forecasting
7. Inventory Optimization
8. AI Insights
9. Generate Reports

---

## 📊 Output

The application generates:

* Forecast Trends
* Inventory Analysis
* Business Recommendations
* KPI Dashboards
* Excel Reports
* PDF Reports

---

## 🎯 Benefits

* Improved Demand Forecasting
* Better Inventory Planning
* Reduced Overstocking
* Reduced Stockouts
* Automated Business Insights
* Faster Decision Making

---

## 👩‍💻 Author

**Sowmya Arigila**

B.Tech Computer Science Engineering

AI-Powered Business Intelligence & Inventory Optimization System
