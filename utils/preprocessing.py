import pandas as pd

def clean_data(df):

    df = df.drop_duplicates()

    for col in df.columns:

        if df[col].dtype == "object":

            df[col].fillna(
                df[col].mode()[0],
                inplace=True
            )

        else:

            df[col].fillna(
                df[col].median(),
                inplace=True
            )

    return df


def convert_dates(df):

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

    return df


def add_date_features(df):

    if "Date" in df.columns:

        df["Year"] = df["Date"].dt.year

        df["Month"] = df["Date"].dt.month

        df["Day"] = df["Date"].dt.day

        df["Quarter"] = (
            df["Date"].dt.quarter
        )

    return df