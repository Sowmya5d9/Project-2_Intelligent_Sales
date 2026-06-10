import pandas as pd
import io

def generate_excel_report(
        dataset,
        forecast,
        inventory
):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        dataset.to_excel(
            writer,
            sheet_name="Dataset",
            index=False
        )

        forecast.to_excel(
            writer,
            sheet_name="Forecast",
            index=False
        )

        inventory.to_excel(
            writer,
            sheet_name="Inventory",
            index=False
        )

    return output.getvalue()