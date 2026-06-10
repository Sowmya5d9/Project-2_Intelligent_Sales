import numpy as np

def safety_stock(
        demand_std,
        service_factor=1.65
):

    return (
        demand_std *
        service_factor
    )


def reorder_point(
        daily_demand,
        lead_time,
        safety_stock_value
):

    return (
        daily_demand *
        lead_time
        +
        safety_stock_value
    )


def eoq(
        annual_demand,
        ordering_cost,
        holding_cost
):

    return np.sqrt(
        (
            2 *
            annual_demand *
            ordering_cost
        )
        /
        holding_cost
    )