import pandas as pd
import plotly.express as px
import analysis.data_modelling as dm

def prep_data(df):

    cols = ['date', 'product_id', 'warehouse_id', 'supplier_id',
            'region', 'units_sold', 'promotion_flag', 'demand_forecast']
    df = df[cols].copy()


    df['difference'] = df['units_sold'] - df['demand_forecast']
    df['abs_difference'] = abs(df['difference'])
    

    df['promo_label'] = df['promotion_flag'].map({0: 'No Promotion', 1: 'Promotion'})

    return df

# Basic line chart
def create_static_line_chart(df):
    df_grouped = df.groupby('date', as_index=False)[['units_sold', 'demand_forecast']].sum()
    df_grouped = df_grouped.sort_values(by='date')

    fig = px.line(df_grouped, x='date', y=['units_sold', 'demand_forecast'],
                  title='Total Company Sales vs. Demand Forecast')    
    
    return fig

#Helper function for the callback
def filter_dataframe(df, warehouse, region):
    df_temp = df.copy()
    
    if warehouse != 'All Warehouses':
        df_temp = df_temp[df_temp['warehouse_id'] == warehouse]

    if region != 'All Regions':
        df_temp = df_temp[df_temp['region'] == region]

    return df_temp

# Top 10 errors
def create_worst_performing_chart(df_filtered):
    df_ranked = df_filtered.groupby('product_id', as_index=False)['abs_difference'].sum()
    df_ranked = df_ranked.sort_values(by='abs_difference', ascending=False).head(10)
    df_ranked['product_id'] = df_ranked['product_id'].astype(str)  #otherwise plt draws a continuous number line on the X-axis

    fig = px.bar(df_ranked, x='product_id', y='abs_difference',
                 title='Top 10 SKUs by Total Error Magnitude',
                 color='abs_difference', color_continuous_scale='Reds')
    
    fig.update_layout(plot_bgcolor="white")
    return fig

# Box plot
def create_promo_box_plot(df_filtered):
    fig = px.box(df_filtered, x="promo_label", y="difference", color="promo_label",
                 title="Distribution of Forecast Errors (Bias)")
    
    fig.update_layout(plot_bgcolor="white", showlegend=False)
    fig.update_yaxes(gridcolor='#eee', zeroline=True)
    return fig


