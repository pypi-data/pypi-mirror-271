# data_quality_checks.py

from pyspark.sql import DataFrame
from pyspark.sql.functions import col

def check_missing_values(df):
    """
    Check for missing values in a DataFrame.
    
    Parameters:
    df (DataFrame): Input DataFrame.
    
    Returns:
    dict: Dictionary containing column names with missing values and the number of missing values.
    """
    missing_columns = {col: df.where(col(col_name).isNull()).count() for col_name in df.columns}
    return {col_name: count for col_name, count in missing_columns.items() if count > 0}

def check_data_types(df):
    """
    Check the data types of columns in a DataFrame.
    
    Parameters:
    df (DataFrame): Input DataFrame.
    
    Returns:
    dict: Dictionary containing column names and their corresponding data types.
    """
    data_types = {col_name: str(data_type) for col_name, data_type in df.dtypes}
    return data_types
