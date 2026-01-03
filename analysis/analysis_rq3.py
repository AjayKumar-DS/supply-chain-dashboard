"""
RQ3: Supplier analysis: how do lead times vary between different suppliers? Which are the most 
reliable/whose lead times are most consistent? Is there a correlation between supplier lead times 
and inventory levels?
"""


import analysis.data_modelling as dm
import pandas as pd
import plotly.express as px

# RQ3.1: Average Lead Time by Supplier
def plot_avg_lead_time(df: pd.DataFrame):
    avg_df = (df.groupby("supplier_id", as_index=False)["supplier_lead_time_days"].mean())

    # supplier_id as a category
    avg_df["supplier_id"] = avg_df["supplier_id"].astype(str)

    bar_fig = px.bar(
        avg_df.round(2),
        x="supplier_id",
        y="supplier_lead_time_days",
        title="<b>Average Lead Time by Supplier</b>",
        labels={
            "supplier_id": "Supplier ID",
            "supplier_lead_time_days": "Average Lead Time (days)"
        },
        template="plotly_white",
        height=450
    )
    return bar_fig


# RQ3.2: Lead Time Distribution by Supplier
def plot_lead_time_box(df: pd.DataFrame):
    df_plot = df.copy()
    df_plot["supplier_id"] = df_plot["supplier_id"].astype(str)

    supplier_order = sorted(df_plot["supplier_id"].unique(), key=int)

    box_fig = px.box(
        df_plot,
        x="supplier_id",
        y="supplier_lead_time_days",
        title="<b>Lead Time Distribution by Supplier</b>",
        labels={
            "supplier_id": "Supplier ID",
            "supplier_lead_time_days": "Lead Time (days)"
        },
        template="plotly_white",
        height=450
    )
    box_fig.update_xaxes(categoryorder="array", categoryarray=supplier_order)
    return box_fig

# SUMMARY TABLE
def supplier_summary_table(df: pd.DataFrame):
    summary = (
        df.groupby("supplier_id")["supplier_lead_time_days"].agg(["mean", "median", "min", "max", "std", "count"]).reset_index()
    )

    summary.columns = [
        "Supplier ID",
        "Average Lead Time (Days)",
        "Median Lead Time (Days)",
        "Minimum Lead Time (Days)",
        "Maximum Lead Time (Days)",
        "Lead Time Variability (Std Dev)",
        "Total Orders",
    ]
    return summary.round(2)

# RQ3.3: Lead Time vs Inventory Level
def plot_lead_time_vs_inventory(df: pd.DataFrame):
    inv_df =df.groupby("supplier_id", as_index=False).agg(
            avg_lead_time=("supplier_lead_time_days", "mean"),
            avg_inventory=("inventory_level", "mean")
        )

    scatter_fig = px.scatter(
        inv_df.round(2),
        x="avg_lead_time",
        y="avg_inventory",
        text="supplier_id",
        title="<b>Average Lead Time vs Inventory Level</b>",
        labels={
            "avg_lead_time": "Average Lead Time (days)",
            "avg_inventory": "Average Inventory Level"
        },
        trendline="ols",
        template="plotly_white",
        height=450
    )

    scatter_fig.update_traces(
        textposition="top center",
        marker=dict(size=10)
    )
    scatter_fig.update_traces(
        selector=dict(mode="lines"),
        line=dict(color="#2A3F5F", dash="dash")
    )

    return scatter_fig

