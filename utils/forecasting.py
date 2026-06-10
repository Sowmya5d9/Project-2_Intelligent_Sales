import pandas as pd
from datetime import timedelta

def forecast_sales(
        model,
        data,
        feature_columns,
        forecast_days=30
):

    future_data = []

    for _ in range(forecast_days):

        row = {}

        for col in feature_columns:

            row[col] = data[col].mean()

        future_data.append(row)

    future_df = pd.DataFrame(
        future_data
    )

    predictions = model.predict(
        future_df
    )

    last_date = pd.Timestamp.today()

    forecast_df = pd.DataFrame({
        "Date": [
            last_date + timedelta(days=i)
            for i in range(
                1,
                forecast_days + 1
            )
        ],
        "Forecasted_Sales":
            predictions
    })

    return forecast_df 