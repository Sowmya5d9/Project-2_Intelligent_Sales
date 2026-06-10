import pandas as pd
import numpy as np

def generate_pharmacy_data(rows=100):

    np.random.seed(42)

    medicines = [
        "Paracetamol",
        "Cetirizine",
        "Azithromycin",
        "Vitamin C",
        "Metformin",
        "Insulin",
        "Pantoprazole",
        "Dolo 650"
    ]

    regions = [
        "Bangalore",
        "Mysore",
        "Hubli",
        "Mangalore"
    ]

    dates = pd.date_range(
        start="2024-01-01",
        periods=rows
    )

    data = []

    for i in range(rows):

        units = np.random.randint(
            20,
            200
        )

        price = np.random.randint(
            5,
            50
        )

        data.append([
            dates[i],
            np.random.choice(medicines),
            np.random.choice(regions),
            units,
            price,
            units * price,
            np.random.randint(
                100,
                1000
            )
        ])

    df = pd.DataFrame(
        data,
        columns=[
            "Date",
            "Medicine_Name",
            "Region",
            "Units_Sold",
            "Unit_Price",
            "Revenue",
            "Inventory_Level"
        ]
    )

    return df