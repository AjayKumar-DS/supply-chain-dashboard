import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

### Your modules
import analysis.data_modelling as dm  # loading in data_modeling.py
import analysis.analysis_rq1 as vis_rq1
import analysis.analysis_rq2 as vis_rq2
import analysis.analysis_rq3 as vis_rq3
import analysis.analysis_rq4 as vis_rq4
import analysis.analysis_rq5 as vis_rq5


# Load and clean the data
df = pd.read_csv("./data/supply_chain_dataset1.csv")

# Apply data cleaning and transformation
dm.clean_data(df)
dm.changing_columns_name_values(df)

# RQ1:
title_rq1 = "RQ1: What is the distribution of genres on Netflix?"
text_rq1 = "This analysis explores the frequency of different genres available on Netflix to understand content diversity and audience preferences."
fig_rq1 = None  # vis_rq1.plot_genre_distribution(genre_distribution)
rq1_plot_id = "genre-plot"

# RQ2:
title_rq2 = "RQ2: YOUR TITLE HERE"
text_rq2 = "YOUR THOROUGH EXPLANATION HERE"
fig_rq2 = None  # YOUR CODE
rq2_plot_id = "your-plot"

# RQ:3
title_rq3 = "RQ2: YOUR TITLE HERE"
text_rq3 = "YOUR THOROUGH EXPLANATION HERE"
fig_rq3 = None  # YOUR CODE
rq3_plot_id = "your-plot"

# RQ4:
title_rq4 = "RQ2: YOUR TITLE HERE"
text_rq4 = "YOUR THOROUGH EXPLANATION HERE"
fig_rq4 = None  # YOUR CODE
rq4_plot_id = "your-plot"

# RQ5:
title_rq5 = "RQ2: YOUR TITLE HERE"
text_rq5 = "YOUR THOROUGH EXPLANATION HERE"
fig_rq5 = None  # YOUR CODE
rq5_plot_id = "your-plot"

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        # Dashboard Title
        html.H1("The title of your Dashboard", className="text-center my-4"),
        # Research Question 1
        dbc.Row(
            dbc.Col(html.H3(title_rq1, className="text-center text-primary"), width=12),
            className="mb-3",
        ),
        dbc.Row(
            dbc.Col(html.P(text_rq1, className="text-center lead"), width=12),
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id=rq1_plot_id, figure=fig_rq1), width=12),
            className="mb-5",
        ),
        # Research Question 2
        dbc.Row(
            dbc.Col(html.H3(title_rq2, className="text-center text-primary"), width=12),
            className="mb-3",
        ),
        dbc.Row(
            dbc.Col(html.P(text_rq2, className="text-center lead"), width=12),
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id=rq2_plot_id, figure=fig_rq2), width=12),
            className="mb-5",
        ),
        # Placeholder for more research questions
        # Repeat the same pattern for RQ2, RQ3, etc.
        # UNCOMMENT AND MODIFY THE FOLLOWING LINES FOR EACH ADDITIONAL RQ
        # Research Question X
        # dbc.Row(
        #    dbc.Col(html.H3(title_rqX,
        #                    className="text-center text-primary"), width=12),
        #    className="mb-3"
        # ),
        # dbc.Row(
        #    dbc.Col(html.P(
        #        text_rqX,
        #        className="text-center lead"), width=12),
        #    className="mb-4"
        # ),
        # dbc.Row(
        #    dbc.Col(dcc.Graph(id=rqX_plot_id, figure=fig_rqX), width=12),
        #    className="mb-5"
        # ),
    ],
    fluid=True,
)

### You can create callbacks here if needed for interactivity
### For example, if you want to update plots based on user input
### You can define your callbacks below
### It is optional. Bonus points if you implement interactivity!!!

# # Set up layout - combine both layouts
# app.layout = html.Div([
#     supchaingg(),  # From final_project.py
#     inventory_layout(df, app)  # From inventory.py, pass df and app
# ])

if __name__ == "__main__":
    app.run(debug=True)
