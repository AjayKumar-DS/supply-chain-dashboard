"""
Babak - Inventory/replenishment.
1: Are the inventory levels of products aligned with the sales demand?
2: How many weeks of inventory cover do the products have?
3: Is the re-order point appropriate based on the actual demand? - Babak

"""

import numpy as np
import pandas as pd
import plotly.express as px

def plot_inventory_vs_sales_time(df: pd.DataFrame, product_id: str, warehouse_id: str):
    """
    Are inventory levels aligned with sales demand?
    Shows units_sold and inventory_level over time for one product at one warehouse.
    """
    data = df[(df["product_id"] == product_id) & (df["warehouse_id"] == warehouse_id)].copy()

    if data.empty:
        # Return empty fig, without trashing
        return px.line(title="No data for selected product/warehouse")

    plot_df = data[["date", "units_sold", "inventory_level"]].melt(
        id_vars="date",
        value_vars=["units_sold", "inventory_level"],
        var_name="Metric",
        value_name="Value",
    )

    fig = px.line(
        plot_df,
        x="date",
        y="Value",
        color="Metric",
        title=f"Inventory vs. Sales over time – {product_id} @ {warehouse_id}",
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Units")
    return fig


def plot_weeks_of_inventory_cover(df: pd.DataFrame, top_n: int = 20):
    grouped = df.groupby(["product_id", "warehouse_id"], as_index=False).agg(
        avg_daily_sales=("units_sold", "mean"),
        avg_inventory=("inventory_level", "mean"),
    )

    grouped["weeks_cover"] = grouped["avg_inventory"] / (grouped["avg_daily_sales"] * 7)
    grouped.loc[grouped["avg_daily_sales"] <= 0, "weeks_cover"] = np.nan

    grouped = grouped.sort_values("avg_daily_sales", ascending=False).head(top_n)

    grouped["product_id"] = grouped["product_id"].astype(str)
    grouped["warehouse_id"] = grouped["warehouse_id"].astype(str)

    fig = px.bar(
        grouped,
        x="product_id",
        y="weeks_cover",
        color="warehouse_id",
        title=f"Weeks of Inventory Cover (top {top_n} product/warehouse combinations)",
        barmode="group",
    )

    fig.update_layout(
        barmode="group",
        xaxis_title="Product",
        yaxis_title="Weeks of cover",
    )

    return fig


def plot_reorder_point_vs_leadtime_demand(df: pd.DataFrame, top_n: int = 200):
    """
    Is the re-order point appropriate based on the actual demand?
    Compares reorder_point with demand during lead time:
        demand_lead_time = avg_daily_sales * avg_lead_time
    """
    grouped = df.groupby(["product_id", "warehouse_id"], as_index=False).agg(
        avg_daily_sales=("units_sold", "mean"),
        avg_lead_time=("supplier_lead_time_days", "mean"),
        reorder_point=("reorder_point", "mean"),
    )

    grouped["demand_lead_time"] = grouped["avg_daily_sales"] * grouped["avg_lead_time"]

    grouped["status"] = np.where(
        grouped["reorder_point"] >= grouped["demand_lead_time"],
        "Reorder ≥ Demand",
        "Reorder < Demand",
    )

    grouped = grouped.sort_values("avg_daily_sales", ascending=False).head(top_n)

    fig = px.scatter(
        grouped,
        x="demand_lead_time",
        y="reorder_point",
        color="status",
        hover_data=["product_id", "warehouse_id"],
        title="Reorder Point vs. Demand during Lead Time",
    )
    fig.update_layout(
        xaxis_title="Demand during lead time (units)",
        yaxis_title="Reorder point (units)"
    )

    if not grouped.empty:
        min_val = float(grouped["demand_lead_time"].min())
        max_val = float(grouped["demand_lead_time"].max())
        fig.add_shape(
            type="line",
            x0=min_val,
            y0=min_val,
            x1=max_val,
            y1=max_val,
            line=dict(dash="dash"),
        )

    return fig
