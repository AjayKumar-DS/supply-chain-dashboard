import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    
    # remove duplicates
    df = df.drop_duplicates()
    return df

def changing_columns_name_values(data: pd.DataFrame) -> pd.DataFrame:
    # standardize column names
    data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]

    column_data=data.rename(columns={"sku_id":"product_id"})
    column_data["product_id"]=column_data["product_id"].str.replace("SKU_","",).astype(int)
    column_data["warehouse_id"]=column_data["warehouse_id"].str.replace("WH_","").astype(int)
    column_data["supplier_id"]=column_data["supplier_id"].str.replace("SUP_","").astype(int)

    # convert Date column to datetime
    column_data["date"] = pd.to_datetime(column_data["date"],dayfirst=True, errors="coerce")

    #Drop rows with invalid data
    column_data = column_data.drop(columns=["stockout_flag"])

    # handle missing values (fill missing values with 'unknown')
    column_data = column_data.fillna("Unknown")
    return column_data


