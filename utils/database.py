import sqlite3
import pandas as pd

DB_NAME = "sales_forecasting.db"

def create_connection():
    return sqlite3.connect(DB_NAME)

def save_dataframe(df, table_name):
    conn = create_connection()
    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )
    conn.close()

def load_dataframe(table_name):
    conn = create_connection()

    try:
        df = pd.read_sql(
            f"SELECT * FROM {table_name}",
            conn
        )

    except:
        df = pd.DataFrame()

    conn.close()

    return df

def get_tables():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    )

    tables = cursor.fetchall()

    conn.close()

    return tables