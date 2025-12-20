import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

import analysis.data_modelling as dm
import analysis.analysis_rq1 as vis_rq1
# import analysis.analysis_rq2 as vis_rq2
import analysis.analysis_rq3 as vis_rq3
# import analysis.analysis_rq4 as vis_rq4
# import analysis.analysis_rq5 as vis_rq5


# Loaded the data
df = pd.read_csv("data/supply_chain_dataset1.csv")

df = dm.clean_data(df)
df = dm.changing_columns_name_values(df)

df_rq1 = vis_rq1.prep_data(df)

suppliers = sorted(df["supplier_id"].unique())


# RQ1 (PLACEHOLDER – UNCHANGED)
title_rq1 = "RQ1: How accurate is the forecast overall, and which products, locations, or promotions are causing the biggest errors?"
text_rq1 = "This analysis explores how accurate the sales predictions are. It finds the biggest errors by product and location, and shows how promotions affect the results."
fig_rq1_line = vis_rq1.create_static_line_chart(df_rq1)
fig_rq1_box = vis_rq1.create_promo_box_plot(df_rq1)
rq1_plot_id = "rq1-plot"

# RQ2 (PLACEHOLDER – UNCHANGED)
title_rq2 = "RQ2: YOUR TITLE HERE"
text_rq2 = "YOUR THOROUGH EXPLANATION HERE"
fig_rq2 = None
rq2_plot_id = "rq2-plot"

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
rq3_plot_id_3 = "rq3-scatter"
rq3_table_id = "rq3-table"


# RQ4 (PLACEHOLDER – UNCHANGED)
title_rq4 = "RQ4: YOUR TITLE HERE"
text_rq4 = "YOUR THOROUGH EXPLANATION HERE"
fig_rq4 = None
rq4_plot_id = "rq4-plot"


# RQ5 (PLACEHOLDER – UNCHANGED)
title_rq5 = "RQ5: YOUR TITLE HERE"
text_rq5 = "YOUR THOROUGH EXPLANATION HERE"
fig_rq5 = None
rq5_plot_id = "rq5-plot"


# INITIALIZE DASH APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# LAYOUT
app.layout = dbc.Container(
    [
        html.H1("Supply Chain Dashboard", className="text-center my-4"),

        # ===================== RQ1 SECTION =====================

        dbc.Row(dbc.Col(html.H3(title_rq1, className="text-center text-primary"))),
        dbc.Row(dbc.Col(html.P(text_rq1, className="text-center lead"))),

        # Static Line Chart
        dbc.Row(dbc.Col(dcc.Graph(figure=fig_rq1_line))),
        html.Hr(),

        # Filters 
        html.Label("Select Warehouse:"),
        dcc.Dropdown(
            id="rq1-warehouse-dropdown",
            options=["All Warehouses"] + sorted(df['warehouse_id'].unique().tolist()),
            value='All Warehouses',
            clearable=False
        ),
        
        html.Br(), # Simple line break
        
        html.Label("Select Region:"),
        dcc.Dropdown(
            id="rq1-region-dropdown",
            options=["All Regions"] + sorted(df['region'].unique().tolist()),
            value='All Regions',
            clearable=False
        ),

        html.Br(),

        # Dynamic Bar Chart
        html.H4("Top 10 Worst Performing SKUs"),
        dbc.Row(dbc.Col(dcc.Graph(id="rq1-worst-performing-bar"))),

        html.Hr(),

        # Box Plot
        html.H4("Forecast Stability (Promotions)"),
        dbc.Row(dbc.Col(dcc.Graph(figure=fig_rq1_box))),

        html.Hr(style={'borderTop': '3px solid #bbb'}), # Separator line

        #========================================================

        # ===================== RQ3 SECTION =====================
        dbc.Row(
            dbc.Col(html.H3(title_rq3, className="text-center text-primary")),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(html.P(text_rq3, className="text-center lead")),
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
            dcc.Graph(id=rq3_plot_id_1),
            width=10
        ),
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
                        html.Div(
                            id=rq3_table_id,
                            style={"overflowX": "auto"}
                        ),
                    ]
                )
            ),
            width=12
        ),
        className="my-4"
    ),

    # Scatter plot
    dbc.Row(
        dbc.Col(
            dcc.Graph(
                id=rq3_plot_id_3,
                figure=vis_rq3.plot_mean_vs_std(df)
            ),
            width=12
        )
    )
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

    df_filtered = vis_rq1.filter_dataframe(df, warehouse_id, region_id)
    
    fig_sku = vis_rq1.create_worst_performing_chart(df_filtered)

    return fig_sku

# CALLBACK (ONLY RQ3 LOGIC)
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
    table = dbc.Table.from_dataframe(
    summary_df,
    striped=True,
    bordered=True,
    hover=True,
    responsive=True
    )
    return fig_bar, fig_box, table

# RUN APP
if __name__ == "__main__":
    app.run(debug=True)
