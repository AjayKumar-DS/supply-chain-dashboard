import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import analysis.data_modelling as dm
import analysis.analysis_rq1 as vis_rq1
import analysis.analysis_rq2 as vis_rq2
import analysis.analysis_rq3 as vis_rq3
import analysis.analysis_rq4 as vis_rq4
import analysis.analysis_rq5 as vis_rq5


# Loaded the data
df = pd.read_csv("data/supply_chain_dataset1.csv")

# Clean data and prepare it for analysis
df = dm.clean_data(df)
df = dm.changing_columns_name_values(df)

# Lists of unique IDs
suppliers = dm.get_unique_supplier_id(df)
warehouses = dm.get_unique_warehouse_id(df)
regions = dm.get_unique_region(df)

# RQ1
title_rq1 = "RQ1: How accurate is the forecast overall, and which products, locations, or promotions are causing the biggest errors?"
text_rq1 = "This analysis explores how accurate the sales predictions are. It finds the biggest errors by product and location, and shows how promotions affect the results."
df_rq1 = vis_rq1.prep_data(df)
fig_rq1_line = vis_rq1.create_static_line_chart(df_rq1)
fig_rq1_box = vis_rq1.create_promo_box_plot(df_rq1)
rq1_plot_id = "rq1-plot"

# RQ2
title_rq2 = """RQ2:  How do promotions impact sales volume/profitability? Is there a pattern - when the 
promotions are running or in which regions? How many product promotions are usually running 
at the same time?"""
text_rq2 = """This analysis examines how promotional campaigns affect average sales,
            profitability, and how promotions are distributed across regions."""
df_rq2 = vis_rq2.prepare_promotion_data(df)
fig_promo_sales = vis_rq2.plot_avg_units_sold(df_rq2)
fig_promo_profit = vis_rq2.plot_avg_profit(df_rq2)
fig_promo_region = vis_rq2.plot_promotions_by_region(df_rq2)

# RQ3
title_rq3 = """
    RQ3: How do lead times vary between different suppliers? 
    Which suppliers are most consistent, and is there a relationship 
    between lead time and inventory levels?
    """


text_rq3 = """
    This analysis compares supplier lead times to identify the most reliable 
    suppliers and examines how lead time variability impacts inventory levels.
    """

rq3_plot_id_1 = "rq3-bar"
rq3_plot_id_2 = "rq3-box"
rq3_table_id = "rq3-table"
rq3_plot_id_3 = "rq3-scatter"


# RQ4
title_rq4 = """RQ4: Inventory/replenishment."""

text_rq4 = """ Are the inventory levels of products aligned with the sales demand?
2: How many weeks of inventory cover do the products have?
3: Is the re-order point appropriate based on the actual demand? """

rq4_plot_id = "rq4-plot"


# RQ5
title_rq5 = "RQ5: Sales performance of top products"
text_rq5 = "This analysis explores how the demand for top selling products varies in different regions and months"

rq5_n_products_to_show = 5
rq5_month_from = 1
rq5_month_to = 12

rq5_top_n_products = vis_rq5.get_top_n_products_sold(df, rq5_n_products_to_show)

rq5_sq2_sale_performance_per_region_df = (
    vis_rq5.get_sale_performance_for_products_across_regions(df, rq5_top_n_products, regions)
)
rq5_sq2_graph_id = "sale_across_regions_graph"
rq5_sq2_graph_figure = vis_rq5.plot_sale_performance_for_products_across_regions(
    rq5_sq2_sale_performance_per_region_df
)

rq5_sq3_demand_per_month_df = vis_rq5.get_demand_per_month(
    df, rq5_top_n_products, rq5_month_from, rq5_month_to
)
rq5_sq3_demand_per_month_graph_id = "demand_over_time_graph"
rq5_sq3_demand_per_month_graph_figure = vis_rq5.plot_demand_per_month(
    rq5_sq3_demand_per_month_df
)


# INITIALIZE DASH APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# LAYOUT
app.layout = dbc.Container(
    [
        html.H1("Supply Chain Dashboard", className="text-center my-4"),

        # ===================== RQ1 SECTION =====================

        # Title
        dbc.Row(
            dbc.Col(html.H3(title_rq1, 
                            className="text-center text-primary"), width=12),
            className="mb-3"
        ),

        # Text Description
        dbc.Row(
            dbc.Col(html.P(text_rq1, 
                           className="text-center lead"), width=12),
            className="mb-4"
        ),

        # Line Chart
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_rq1_line), width=12),
            className="mb-5"
        ),

        # Filters
        dbc.Row(
            [
                dbc.Col([
                    html.Label("Select Warehouse:"),
                    dcc.Dropdown(
                        id="rq1-warehouse-dropdown",
                        options=["All Warehouses"] + list(warehouses),
                        value='All Warehouses',
                        clearable=False
                    )
                ], width=6),

                dbc.Col([
                    html.Label("Select Region:"),
                    dcc.Dropdown(
                        id="rq1-region-dropdown",
                        options=["All Regions"] + list(regions),
                        value='All Regions',
                        clearable=False
                    )
                ], width=6),
            ],
            className="mb-5"
        ),

        # Dynamic Bar Chart
        dbc.Row(
            dbc.Col(html.H4("Top 10 Worst Performing SKUs"), width=12),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="rq1-worst-performing-bar"), width=12),
            className="mb-5"
        ),

        # Box Plot
        dbc.Row(
            dbc.Col(html.H4("Forecast Stability (Promotions)"), width=12),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(figure=fig_rq1_box), width=12),
            className="mb-4"
        ),

        #========================================================

        # ===================== RQ2 SECTION =====================

        html.Hr(),
        # Title
        dbc.Row(
            dbc.Col(html.H3(title_rq2, className="text-center text-primary"), width=12),
            className="mb-3"
        ),

        # Text Description
        dbc.Row(
            dbc.Col(html.P(text_rq2, className="text-center lead"), width=12),
            className="mb-4"
        ),
        dbc.Row(dbc.Col(dcc.Graph(figure=fig_promo_sales), width=12)),
        dbc.Row(dbc.Col(dcc.Graph(figure=fig_promo_profit), width=12)),
        dbc.Row(dbc.Col(dcc.Graph(figure=fig_promo_region), width=12)),

        #========================================================

        # ===================== RQ3 SECTION =====================
        html.Hr(),
        # Title
        dbc.Row(
            dbc.Col(html.H3(title_rq3, className="text-center text-primary"), width=12),
            className="mb-3"
        ),

        # Text Description
        dbc.Row(
            dbc.Col(html.P(text_rq3, className="text-center lead"), width=12),
            className="mb-4"
        ),

        # Dropdown and Bar chart
        dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Select Supplier(s)"),
                        dbc.CardBody(
                            dcc.Dropdown(
                                id="rq3-supplier-dropdown",
                                options=[{"label": str(s), "value": s} for s in suppliers],
                                multi=True,
                                placeholder="Select supplier(s)"
                            )
                        ),
                    ]
                ),
                width=2
            ),
            dbc.Col(
                dcc.Graph(id=rq3_plot_id_1),width=10),
            ],
            className="mb-4"
        ),

        # Box plot
        dbc.Row(dbc.Col(dcc.Graph(id=rq3_plot_id_2), className="mb-3",width=12)),

        # Summary table
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.B("Supplier Summary Table",className="fw-bold text-center mb-2"),
                            html.Div(id=rq3_table_id,style={"overflowX": "auto"}),
                        ]
                    )
                ),
                width=12
            ),
            className="my-4"
        ),

        # Scatter plot
        dbc.Row(dbc.Col(dcc.Graph(id=rq3_plot_id_3, figure=vis_rq3.plot_lead_time_vs_inventory(df)),width=12),
            className="mb-4"
        ),

        #========================================================
        # ===================== RQ4 SECTION =====================

        html.Hr(),
        dbc.Row(dbc.Col(html.H2(title_rq4, className="text-center text-primary mt-3"))),
        dbc.Row(dbc.Col(html.P(text_rq4, className="text-center lead"))),

        # Product & Warehouse dropdown part
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select Product:"),
                        dcc.Dropdown(
                            id="rq4-sku-dropdown",
                            options=[
                                {"label": str(p), "value": p}
                                for p in sorted(df["product_id"].dropna().unique())
                            ],
                            value=sorted(df["product_id"].dropna().unique())[0],
                            clearable=False,
                        )
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        html.Label("Select Warehouse:"),
                        dcc.Dropdown(
                            id="rq4-warehouse-dropdown",
                            options=[
                                {"label": str(w), "value": w}
                                for w in sorted(df["warehouse_id"].dropna().unique())
                            ],
                            value=sorted(df["warehouse_id"].dropna().unique())[0],
                            clearable=False
                        )
                    ],
                    width=6
                )
            ],
            className="mb-4"
        ),

        dbc.Row(dbc.Col(dcc.Graph(id="rq4-sawplot"), width=12), className="mb-4"),
        dbc.Row(dbc.Col(dcc.Graph(id="rq4-bars"), width=12), className="mb-4"),
        dbc.Row(dbc.Col(dcc.Graph(id="rq4-scatter"), width=12), className="mb-4"),

        # ===================== RQ5 SECTION =====================
        html.Hr(),
        dbc.Row(dbc.Col(html.H2(title_rq5, className="text-center text-primary mt-3"))),
        dbc.Row(dbc.Col(html.P(text_rq5, className="text-center lead"))),

        # Filters
        dbc.Row(
            dbc.Col(
                html.H3("Filters", className="text-center text-primary"),
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(html.Label("Number of top products to show"), width=12, className="text-center mb-3")
        ),
        dbc.Row(
            dbc.Col(
                vis_rq5.get_number_of_products_filter_selector(
                    rq5_n_products_to_show
                ),
                width=3,
                className="mx-auto"
            ),
            className="mb-5",
        ),

        # Sales performance across regions
        dbc.Row(
            dbc.Col(
                html.H3(
                    "How does sales performance for the top products vary across different regions?",
                    className="text-center text-primary",
                ),
                width=12,
            ),
            className="mb-3",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id=rq5_sq2_graph_id, figure=rq5_sq2_graph_figure),
                width=12
            ),
            className="mb-5",
        ),
        # Demand change over period of time
        dbc.Row(
            dbc.Col(
                html.H3(
                    "Does the demand for top products change over time, and are there noticeable sales peaks?",
                    className="text-center text-primary",
                ),
                width=12,
            ),
            className="mb-3",
        ),
        # Date filter only applied for this question
        dbc.Row(dbc.Col(html.Label("Month range"), width=12, className="text-center mb-3")),
        dbc.Row(
            dbc.Col(
                vis_rq5.get_month_range_filter_selector(
                    rq5_month_from, rq5_month_to
                ),
                width=6,
                className="mx-auto"
            ),
            className="mb-3",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id=rq5_sq3_demand_per_month_graph_id,
                    figure=rq5_sq3_demand_per_month_graph_figure,
                ),
                width=12
            ),
        ),
        #========================================================
    ],
    fluid=True
)

#CALLBACK (RQ1)
@app.callback(
    Output("rq1-worst-performing-bar", "figure"),
    [Input('rq1-warehouse-dropdown', "value"),
     Input('rq1-region-dropdown', "value")]
)
def update_rq1_bar_chart(warehouse_id, region_id):

    df_filtered = vis_rq1.filter_dataframe(df_rq1, warehouse_id, region_id)

    fig_sku = vis_rq1.create_worst_performing_chart(df_filtered)

    return fig_sku

# CALLBACK (RQ3)
@app.callback(
    Output(rq3_plot_id_1, "figure"),
    Output(rq3_plot_id_2, "figure"),
    Output(rq3_table_id, "children"),
    Input("rq3-supplier-dropdown", "value"),
)
def update_rq3(selected_suppliers):

    if selected_suppliers:
        filtered_df = df[df["supplier_id"].isin(selected_suppliers)]
    else:
        filtered_df = df

    fig_bar = vis_rq3.plot_avg_lead_time(filtered_df)
    fig_box = vis_rq3.plot_lead_time_box(filtered_df)

    summary_df = vis_rq3.supplier_summary_table(filtered_df)
    table = dbc.Table.from_dataframe(summary_df, striped=True, bordered=True, hover=True, responsive=True)
    return fig_bar, fig_box, table


#CALLBACK (Rq-4)
@app.callback(
    Output("rq4-sawplot", "figure"),
    Output("rq4-bars", "figure"),
    Output("rq4-scatter", "figure"),
    Input("rq4-sku-dropdown", "value"),
    Input("rq4-warehouse-dropdown", "value")
)
def update_rq4(product_id, warehouse_id):
    fig_saw = vis_rq4.plot_inventory_vs_sales_time(df, product_id, warehouse_id)
    fig_bars = vis_rq4.plot_weeks_of_inventory_cover(df, top_n=20)
    fig_scatter = vis_rq4.plot_reorder_point_vs_leadtime_demand(df, top_n=200)
    return fig_saw, fig_bars, fig_scatter




# CALLBACK (RQ5)
@app.callback(
    Output(rq5_sq2_graph_id, "figure"), [Input("rq5_top_products_filter", "value")]
)
def rq5_update_sales_per_region_chart(number_of_products_to_show):
    # filter dataset for new number of products
    products_to_plot = vis_rq5.get_top_n_products_sold(df, number_of_products_to_show)

    # create data structure for products included
    products_to_plot_df = vis_rq5.get_sale_performance_for_products_across_regions(
        df, products_to_plot, regions
    )

    # create figure from data structure
    new_graph = vis_rq5.plot_sale_performance_for_products_across_regions(
        products_to_plot_df
    )
    return new_graph

# update performance per month
@app.callback(
    Output(rq5_sq3_demand_per_month_graph_id, "figure"),
    [Input("rq5_top_products_filter", "value"), Input("rq5_months_filter", "value")],
)
def rq5_update_sales_per_month_graph(number_of_products_to_show, month_range):
    month_from = month_range[0]
    month_to = month_range[1]

    # filter dataset for new number of products and month range
    products_to_plot = vis_rq5.get_top_n_products_sold(df, number_of_products_to_show)

    # create data structure for products included
    products_to_plot_df = vis_rq5.get_demand_per_month(
        df, products_to_plot, month_from, month_to
    )

    # create figure from data structure
    new_graph = vis_rq5.plot_demand_per_month(products_to_plot_df)
    return new_graph

# RUN APP
if __name__ == "__main__":
    app.run(debug=True)
