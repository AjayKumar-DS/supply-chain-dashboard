import analysis.data_modelling as dm
import pandas as pd
import plotly.express as px

# DATA PREPARATION
def prepare_promotion_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Label promotions
    df["promotion_flag"] = df["promotion_flag"].map(
        {0: "No Promotion", 1: "Promotion"}
    )

    # Calculate profit
    df["profit"] = (df["unit_price"] - df["unit_cost"]) * df["units_sold"]

    return df


# RQ: Sales impact of promotions
def plot_avg_units_sold(df: pd.DataFrame):
    sales_avg = df.groupby("promotion_flag", as_index=False)["units_sold"].mean()

    fig = px.bar(
        sales_avg,
        x="promotion_flag",
        y="units_sold",
        title="<b>Average Units Sold: Promotion vs No Promotion</b>",
        labels={
            "promotion_flag": "Promotion Status",
            "units_sold": "Average Units Sold"
        },
        template="plotly_white",
        height=400
    )
    return fig


# RQ: Profit impact of promotions
def plot_avg_profit(df: pd.DataFrame):
    profit_avg = df.groupby("promotion_flag", as_index=False)["profit"].mean()

    fig = px.bar(
        profit_avg,
        x="promotion_flag",
        y="profit",
        title="<b>Average Profit: Promotion vs No Promotion</b>",
        labels={
            "promotion_flag": "Promotion Status",
            "profit": "Average Profit"
        },
        template="plotly_white",
        height=400
    )
    return fig


# RQ: Regional promotion activity
def plot_promotions_by_region(df: pd.DataFrame):
    region_promos = (
        df[df["promotion_flag"] == "Promotion"]
        .groupby("region", as_index=False)
        .size()
        .rename(columns={"size": "promotion_count"})
    )

    fig = px.bar(
        region_promos,
        x="region",
        y="promotion_count",
        title="<b>Number of Promotions by Region</b>",
        labels={
            "region": "Region",
            "promotion_count": "Promotion Count"
        },
        template="plotly_white",
        height=400
    )
    return fig
