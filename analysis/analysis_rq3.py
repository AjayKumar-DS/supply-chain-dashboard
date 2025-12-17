import analysis.data_modelling as dm

import pandas as pd
import plotly.express as px


# -------------------------------------------------
# RQ1: How do lead times vary between suppliers?
# -------------------------------------------------

def plot_avg_lead_time(df: pd.DataFrame):
    """
    Bar chart showing average lead time for each supplier
    """

    avg_df = df.groupby("supplier_id", as_index=False)["supplier_lead_time_days"].mean()

    fig = px.bar(
        avg_df,
        x="supplier_id",
        y="supplier_lead_time_days",
        title="Average Lead Time by Supplier",
        labels={
            "supplier_id": "Supplier",
            "supplier_lead_time_days": "Average Lead Time (days)"
        },
        template="plotly_white",
        height=450
    )
    fig.update_layout(
    xaxis=dict(
        tickmode="linear",
        dtick=1
        )
    )

    return fig


# -------------------------------------------------
# RQ2: Which suppliers are most consistent?
# -------------------------------------------------

def plot_lead_time_box(df: pd.DataFrame):
    """
    Box plot showing lead time variation per supplier
    """

    fig = px.box(
        df,
        x="supplier_id",
        y="supplier_lead_time_days",
        title="Lead Time Distribution by Supplier",
        labels={
            "supplier_id": "Supplier",
            "supplier_lead_time_days": "Lead Time (days)"
        },
        template="plotly_white",
        height=450
    )
    fig.update_layout(
    xaxis=dict(
        tickmode="linear",
        dtick=1
        )
    )

    return fig


# -------------------------------------------------
# SUMMARY TABLE: Supplier performance overview
# -------------------------------------------------

def supplier_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a summary table for suppliers:
    - average lead time
    - median lead time
    - lead time variability (std dev)
    - number of orders
    """

    summary = df.groupby("supplier_id", as_index=False)["supplier_lead_time_days"].agg(
        min_lead_time="min",
        max_lead_time="max",
        avg_lead_time="mean",
        median_lead_time="median",
        lead_time_std="std",
        order_count="count"
    )

    return summary


# -------------------------------------------------
# RQ3: Relationship between average lead time & consistency
# -------------------------------------------------

def plot_mean_vs_std(df: pd.DataFrame):
    """
    Scatter plot comparing average lead time and variability
    """

    stats = df.groupby("supplier_id", as_index=False)["supplier_lead_time_days"] \
              .agg(mean_lt="mean", std_lt="std")

    fig = px.scatter(
        stats,
        x="mean_lt",
        y="std_lt",
        text="supplier_id",
        title="Average Lead Time vs Consistency",
        labels={
            "mean_lt": "Average Lead Time (days)",
            "std_lt": "Lead Time Variability"
        },
        template="plotly_white",
        height=420
    )

    return fig


# -------------------------------------------------
# RQ4: Is lead time related to inventory levels?
# -------------------------------------------------

def plot_lead_time_vs_inventory(df: pd.DataFrame):
    """
    Scatter plot showing lead time vs inventory (if available)
    """


    inv_df = df.groupby("supplier_id", as_index=False).agg(
        mean_lt=("supplier_lead_time_days", "mean"),
        avg_inventory=("inventory_level", "mean")
    )

    fig = px.scatter(
        inv_df,
        x="mean_lt",
        y="avg_inventory",
        text="supplier_id",
        title="Average Lead Time vs Inventory Level",
        labels={
            "mean_lt": "Average Lead Time (days)",
            "avg_inventory": "Average Inventory"
        },
        template="plotly_white",
        height=420
    )

    return fig
