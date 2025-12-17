"""
Babak - Inventory/replenishment.
1: Are the inventory levels of products aligned with the sales demand?
2: How many weeks of inventory cover do the products have?
3: Is the re-order point appropriate based on the actual demand? - Babak

"""

import numpy as np
import pandas as pd
import plotly.express as px


def plot_inventory_vs_sales_time(df: pd.DataFrame, sku_id: str, warehouse_id: str):
    """
    Are inventory levels aligned with sales demand?
    Shows Units_Sold and Inventory_Level over time for one SKU at one warehouse.
    """
    # Filter data for a single SKU and warehouse
    data = df[(df["SKU_ID"] == sku_id) & (df["Warehouse_ID"] == warehouse_id)].copy()

    if data.empty:
        raise ValueError("No rows found for this combination of SKU_ID and Warehouse_ID.")

    # Convert to long format so we can plot two lines (sales and inventory)
    plot_df = data[["Date", "Units_Sold", "Inventory_Level"]].melt(
        id_vars="Date",
        value_vars=["Units_Sold", "Inventory_Level"],
        var_name="Metric",
        value_name="Value",
    )

    fig = px.line(
        plot_df,
        x="Date",
        y="Value",
        color="Metric",
        title=f"Inventory vs. Sales over time – {sku_id} @ {warehouse_id}",
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Units"
    )

    return fig


def plot_weeks_of_inventory_cover(df: pd.DataFrame, top_n: int = 20):
    """
    How many weeks of inventory cover do the products have?
    Calculates average weeks of cover per (SKU, Warehouse) and
        shows the top_n (by average daily sales) as a bar chart.
    """
    # Aggregate by SKU and Warehouse
    grouped = df.groupby(["SKU_ID", "Warehouse_ID"], as_index=False).agg(
        avg_daily_sales=("Units_Sold", "mean"),
        avg_inventory=("Inventory_Level", "mean"),
    )

    # Weeks of cover = avg_inventory / (avg_daily_sales * 7)
    grouped["Weeks_Cover"] = grouped.apply(
        lambda row: row["avg_inventory"] / (row["avg_daily_sales"] * 7)
        if row["avg_daily_sales"] > 0
        else np.nan,
        axis=1,
    )

    # Select the combinations with the highest average daily sales
    grouped = grouped.sort_values("avg_daily_sales", ascending=False).head(top_n)

    fig = px.bar(
        grouped,
        x="SKU_ID",
        y="Weeks_Cover",
        color="Warehouse_ID",
        barmode="group",
        title=f"Weeks of Inventory Cover (top {top_n} SKU/Warehouse combinations)",
    )
    fig.update_layout(
        xaxis_title="SKU_ID",
        yaxis_title="Weeks of cover"
    )

    return fig


def plot_reorder_point_vs_leadtime_demand(df: pd.DataFrame, top_n: int = 200):
    """
    Is the re-order point appropriate based on the actual demand?
    Compares Reorder_Point with demand during lead time:
        Demand_Lead_Time = avg_daily_sales * avg_lead_time
    """
    # Aggregate by SKU and Warehouse
    grouped = df.groupby(["SKU_ID", "Warehouse_ID"], as_index=False).agg(
        avg_daily_sales=("Units_Sold", "mean"),
        avg_lead_time=("Supplier_Lead_Time_Days", "mean"),
        reorder_point=("Reorder_Point", "mean"),
    )

    # Demand during lead time
    grouped["Demand_Lead_Time"] = grouped["avg_daily_sales"] * grouped["avg_lead_time"]

    # Label whether reorder point is above or below demand in lead time
    grouped["Status"] = np.where(
        grouped["reorder_point"] >= grouped["Demand_Lead_Time"],
        "Reorder ≥ Demand",
        "Reorder < Demand",
    )

    # Again, focus on the most relevant combinations (highest daily sales)
    grouped = grouped.sort_values("avg_daily_sales", ascending=False).head(top_n)

    fig = px.scatter(
        grouped,
        x="Demand_Lead_Time",
        y="reorder_point",
        color="Status",
        hover_data=["SKU_ID", "Warehouse_ID"],
        title="Reorder Point vs. Demand during Lead Time",
    )
    fig.update_layout(
        xaxis_title="Demand during lead time (units)",
        yaxis_title="Reorder point (units)"
    )

    # Add a reference line y = x (where reorder point equals demand in lead time)
    min_val = float(grouped["Demand_Lead_Time"].min())
    max_val = float(grouped["Demand_Lead_Time"].max())

    fig.add_shape(
        type="line",
        x0=min_val,
        y0=min_val,
        x1=max_val,
        y1=max_val,
        line=dict(dash="dash"),
    )

    return fig
