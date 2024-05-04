# data_quality_checks.py

import pandas as pd

def check_missing_values(df):
    """
    Check for missing values in a DataFrame.
    
    Parameters:
    df (pandas.DataFrame): Input DataFrame.
    
    Returns:
    dict: Dictionary containing column names with missing values and the number of missing values.
    """
    missing_values = df.isnull().sum()
    missing_columns = missing_values[missing_values > 0]
    return missing_columns.to_dict()

def check_data_types(df):
    """
    Check the data types of columns in a DataFrame.
    
    Parameters:
    df (pandas.DataFrame): Input DataFrame.
    
    Returns:
    dict: Dictionary containing column names and their corresponding data types.
    """
    data_types = df.dtypes
    return data_types.to_dict()
