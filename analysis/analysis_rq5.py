import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import analysis.data_modelling as dm

def get_top_n_products_sold(df: pd.DataFrame, number_of_products: int) -> pd.DataFrame:
    """
    Gets n most sold products by units sold across all regions.

    :param df: a dataframe with supply chain data set
    :type df: pd.DataFrame

    :param number_of_products: number of products to return.
    :type number_of_products: int

    :return: a dataframe containing n top products by units sold.
    The dataframe has two columns - product_id and units_sold
    """

    # Pseudo code
    # Create empty dictionary for units_sold_per_product
    # Go line by line through the data set
    # For each line, use column product_id as dictionary key, and column units_sold as value (int)
    # If units_sold_per_product dictionary doesn't have the key yet, add it with units_sold = 0
    # Add value from units_sold column, to the value already in units_sold_per_product dictionary

    # define column names
    column_product_id_name = "product_id"
    column_units_sold_name = "units_sold"

    # df.values cannot be used in combination with string column names to get values from the row
    # use get_loc to get index of each column
    column_product_id_index = df.columns.get_loc(column_product_id_name)
    column_units_sold_index = df.columns.get_loc(column_units_sold_name)

    # empty dictionary for sale statistics
    units_sold_per_product_dict = dict()

    # go through all rows - df.values sets row to be list of values in that row
    for row in df.values:
        product_id = row[column_product_id_index]
        units_sold = row[column_units_sold_index]

        # if product_id already exists in dictionary, add up the units sold
        if product_id in units_sold_per_product_dict:
            units_sold_per_product_dict[product_id] += units_sold
        else:
            units_sold_per_product_dict[product_id] = units_sold

    # from the dictionary, create a pandas df that has a column with product_id and a column with units_sold
    # order the df by units_sold descending
    units_sold_per_product_df = pd.DataFrame(
        units_sold_per_product_dict.items(),
        columns=[column_product_id_name, column_units_sold_name],
    ).sort_values(by=column_units_sold_name, ascending=False)

    # take first number_of_products items
    units_sold_per_product_df = units_sold_per_product_df.head(number_of_products)

    return units_sold_per_product_df

def get_number_of_products_filter_selector(number_of_products: int):
    """
    Gets selector for number of products filter

    :param number_of_products: number of products to show
    :type number_of_products: int

    :return: filter selector
    """

    # https://dash.plotly.com/dash-core-components/dropdown
    return dcc.Dropdown(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        number_of_products,
        id="rq5_top_products_filter",
    )


# sale performance across regions
def get_sale_performance_for_products_across_regions(
    df: pd.DataFrame, products_to_include: pd.DataFrame, regions: set[str]
) -> dict:
    """
    Gets sale performance for selected products across regions.

    :param df: a dataframe with supply chain data set
    :type df: pd.DataFrame

    :param products_to_include: products to include from function get_top_n_products.
    :type products_to_include: pd.DataFrame
    
    :param regions: all regions in the data set
    :type regions: set[str]

    :return: a dictionary containing units sold per region per product, where product_id is dictionary key.
    The value of the dictionary is a dictionary, where key is region, and value is units sold in that region.
    """

    # Pseudo code
    # Create list of product IDs to check, from products_to_include
    # Create a dictionary with product IDs where key is product ID, and value is dictionary with all regions and sales in those regions
    # Go through the data set, line by line
    # For each line, use column region to get the region, and units_sold as value (int)
    # Add value from units_sold column to the dictionary

    # define column names
    column_product_id_name = "product_id"
    column_units_sold_name = "units_sold"
    column_region_name = "region"

    # df.values cannot be used in combination with string column names to get values from the row
    # use get_loc to get index of each column
    column_product_id_index = df.columns.get_loc(column_product_id_name)
    column_units_sold_index = df.columns.get_loc(column_units_sold_name)
    column_region_index = df.columns.get_loc(column_region_name)

    # get list of products to include - only use keys from the dictionary,
    # units_sold is not needed (it is total units sold)
    product_ids_to_include = products_to_include[column_product_id_name].unique().tolist()

    # create dictionary to use for results
    perf_per_region_dict = dict()
    for product_id in product_ids_to_include:
        # create dictionary for a product where each region starts with units_sold set to 0
        product_dictionary = dict()
        for region in regions:
            product_dictionary[region] = 0
        perf_per_region_dict[product_id] = product_dictionary

    # count units sold per region
    for row in df.values:
        # get all necessary values from the row
        product_id = row[column_product_id_index]
        units_sold = row[column_units_sold_index]
        region = row[column_region_index]

        # skip products that are not most sold
        if product_id not in product_ids_to_include:
            continue

        # add units sold to sales for region
        perf_per_region_dict[product_id][region] += units_sold

    return perf_per_region_dict


def plot_sale_performance_for_products_across_regions(
    performance_per_region: dict,
) -> px:
    # plotly cannot work with dictionary - convert data to pd DataFrame
    # each region/productId combination is an entry

    # create simple DataFrame where product_id are columns and regions are rows
    df = pd.DataFrame(performance_per_region)

    # use stack function to turn the dataset into structure where
    # regions are columns. reset_index makes sure the columns are actually present in dataframe
    df = df.stack().reset_index()

    # at this point the columns dont have names - rename them
    df.columns = ["region", "product_id", "units_sold"]
    
    # make sure product_id is string to prevent plotly from treating it as numeric range (it does for all integers)
    df["product_id"] = df["product_id"].astype(str)

    fig = px.bar(
        df,
        x="product_id",
        y="units_sold",
        color="region",
        barmode="group",
        labels={"units_sold": "Units Sold", "product_id": "Product ID"},
        title="Units Sold per Product by Region",
        height=600,
        text="region",
    )

    # place labels above bars and not inside
    fig.update_traces(textposition="outside")

    return fig

def get_month_range_filter_selector(from_month: int, to_month: int):
    """
    Gets selector for month range

    :param from_month: month to start from
    :type from_month: int

    :param to_month: month to start end
    :type to_month: int

    :return: filter selector
    """

    MonthNames = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    # https://dash.plotly.com/dash-core-components/rangeslider
    return dcc.RangeSlider(
        id="rq5_months_filter", min=1, max=12, step=1, value=[from_month, to_month], marks=MonthNames
    )


# demand per month
def get_demand_per_month(
    df: pd.DataFrame, products_to_include: pd.DataFrame, from_month: int, to_month: int
) -> dict: 
    """
    Gets sales for selected products per month in defined range.

    :param df: a dataframe with supply chain data set
    :type df: pd.DataFrame

    :param products_to_include: products to include from function get_top_n_products.
    :type products_to_include: pd.DataFrame

    :param from_month: Month to start from (included)
    :type from_month: int

    :param from_to: Month to start from (included)
    :type from_to: int

    :return: a dictionary containing units sold per month per product, where product_id is dictionary key.
    The value of the dictionary is a dictionary, where key is region, and value is units sold in that region.
    """
    
    # Pseudo code
    # Create list of product IDs to check, from products_to_include
    # Create a dictionary with product IDs where key is product ID, and value is dictionary with all months and sales in those months
    # Go through the data set, line by line
    # For each line, use column date to get the month number, and units_sold as value (int). If month is outside of range, skip the row
    # Add value from units_sold column to the dictionary
        
    # define column names
    column_product_id_name = "product_id"
    column_units_sold_name = "units_sold"
    column_date_month_name = "month"

    # df.values cannot be used in combination with string column names to get values from the row
    # use get_loc to get index of each column
    column_product_id_index = df.columns.get_loc(column_product_id_name)
    column_units_sold_index = df.columns.get_loc(column_units_sold_name)
    column_date_month_index = df.columns.get_loc(column_date_month_name)

    # get list of products to include - only use keys from the dictionary,
    # units_sold is not needed (it is total units sold)
    product_ids_to_include = products_to_include[column_product_id_name].unique().tolist()

    # create dictionary to use for results
    perf_per_month_dict = dict()
    for product_id in product_ids_to_include:
        # create dictionary for a product where each month starts with units_sold set to 0
        product_dictionary = dict()
        for month in range(from_month, to_month + 1):
            product_dictionary[month] = 0
        perf_per_month_dict[product_id] = product_dictionary

    # count units sold per month
    for row in df.values:
        product_id = row[column_product_id_index]
        units_sold = row[column_units_sold_index]
        month = row[column_date_month_index]

        # skip products that are not most sold
        if product_id not in product_ids_to_include:
            continue

        # only count sales that are between from and to
        if month >= from_month and month <= to_month:
            perf_per_month_dict[product_id][month] += units_sold

    return perf_per_month_dict


def plot_demand_per_month(demand_per_month: dict) -> px:
    # create simple DataFrame where product_id are columns and regions are rows
    df = pd.DataFrame(demand_per_month)

    # use stack function to turn the dataset into structure where
    # regions are columns. reset_index makes sure the columns are actually present in dataframe
    df = df.stack().reset_index()

    # at this point the columns dont have names - rename them
    df.columns = ["month", "product_id", "units_sold"]
    
    # make sure product_id is string to prevent plotly from treating it as numeric range (it does for all integers)
    df["product_id"] = df["product_id"].astype(str)

    # month should be integer
    df["month"] = df["month"].astype(int)
    
    fig = px.line(
        df,
        x="month",
        y="units_sold",
        color="product_id",
        labels={"units_sold": "Units Sold", "month": "Month"},
        markers=True,
        height=600,
        title="Units Sold per Product per Month"
    )

    # update units_sold axis to be from min. to max. to make sure as much data is visible as 
    # add 100 to make sure there is some space on bottom and top
    min_units_sold = df["units_sold"].min()
    max_units_sold = df["units_sold"].max()
    fig.update_yaxes(range=[min_units_sold - 100, max_units_sold + 100])

    # set increment on X axis to 1 so all values are shown
    # https://plotly.com/python/reference/layout/xaxis/#layout-xaxis-dtick
    fig.update_xaxes(dtick=1)

    return fig
