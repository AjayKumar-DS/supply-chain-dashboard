import analysis.data_modelling as dm
import pandas as pd
import plotly.express as px

# RQ3.1: Average Lead Time by Supplier
def plot_avg_lead_time(df: pd.DataFrame):
    avg_df = (
        df.groupby("supplier_id", as_index=False)["supplier_lead_time_days"]
        .mean()
        .rename(columns={"supplier_lead_time_days": "avg_lead_time"})
    )

    # supplier_id as a category
    avg_df["supplier_id"] = avg_df["supplier_id"].astype(str)

    bar_fig = px.bar(
        avg_df.round(2),
        x="supplier_id",
        y="avg_lead_time",
        title="<b>Average Lead Time by Supplier</b>",
        labels={
            "supplier_id": "Supplier ID",
            "avg_lead_time": "Average Lead Time (days)"
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
        df.groupby("supplier_id")["supplier_lead_time_days"]
        .agg(["mean", "median", "min", "max", "std", "count"])
        .reset_index()
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

# RQ3.3: Mean vs Variability 
def plot_mean_vs_std(df: pd.DataFrame):
    stats = df.groupby("supplier_id", as_index=False)["supplier_lead_time_days"] \
              .agg(mean_lt="mean", std_lt="std")

    scatter_fig = px.scatter(
        stats.round(2),
        x="mean_lt",
        y="std_lt",
        text="supplier_id",
        title="<b>Average Lead Time vs Variability (All Suppliers)</b>",
        labels={
            "mean_lt": "Average Lead Time (days)",
            "std_lt": "Lead Time Variability (Std Dev)"
        },
        template="plotly_white",
        height=450
    )

    scatter_fig.update_traces(
        textposition="top center",
        textfont=dict(size=12, color="black"),
        marker=dict(size=10)
    )
    
    scatter_fig.update_layout(margin=dict(l=60, r=40, t=60, b=60))
    return scatter_fig

