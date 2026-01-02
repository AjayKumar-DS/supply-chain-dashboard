import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans dataset:
    - removes duplicates

    :param df: a dataframe to clean
    :type df: pd.DataFrame

    :return: a cleaned up dataframe
    """
        
    # remove duplicates
    df = df.drop_duplicates()
    return df

def changing_columns_name_values(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms dataset into data structure:
    - column names are lowercase and with _ instead of spaces
    - renames column 'sku_id' to 'product_id'
    - converts columns 'product_id', 'warehouse_id', and 'supplier_id' to number
    - converts column 'date' to date
    - removes 'stockout_flag' column - it has invalid data
    - replaces missing values with 'Unknown'
    - adds month column

    :param df: a dataframe to transform
    :type df: pd.DataFrame

    :return: a cleaned up dataframe
    """

    # standardize column names
    data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]

    column_data=data.rename(columns={"sku_id":"product_id"})
    column_data["product_id"]=column_data["product_id"].str.replace("SKU_","",).astype(int)
    column_data["warehouse_id"]=column_data["warehouse_id"].str.replace("WH_","").astype(int)
    column_data["supplier_id"]=column_data["supplier_id"].str.replace("SUP_","").astype(int)

    # convert Date column to datetime
    column_data["date"] = pd.to_datetime(column_data["date"], errors="coerce")
    column_data["month"] = column_data["date"].dt.month

    #Drop rows with invalid data
    column_data = column_data.drop(columns=["stockout_flag"])

    # handle missing values (fill missing values with 'unknown')
    column_data = column_data.fillna("Unknown")
    return column_data


def get_unique_supplier_id_list(data: pd.DataFrame) -> set[int]:
    """
    Returns a set of unique supplier IDs from data set

    :param data: a dataframe to extract list from
    :type df: pd.DataFrame

    :return: a set of unique supplier IDs
    """
    return set(sorted(data["supplier_id"]))

def get_unique_warehouse_id_list(data: pd.DataFrame) -> set[int]:
    """
    Returns a set of unique warehouse IDs from data set

    :param data: a dataframe to extract list from
    :type df: pd.DataFrame

    :return: a set of unique warehouse IDs
    """
    return set(sorted(data["warehouse_id"]))

def get_unique_region_list(data: pd.DataFrame) -> set[str]:
    """
    Returns a set of unique regions

    :param data: a dataframe to extract list from
    :type df: pd.DataFrame

    :return: a set of unique regions
    """
    return set(sorted(data["region"]))