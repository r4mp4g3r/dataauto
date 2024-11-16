# dataauto/data_cleaner.py

import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

def clean_data(df, strategy='mean', columns=None):
    """
    Handle missing values in specified columns using the given strategy.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        strategy (str): Strategy to fill missing values ('mean', 'median', 'mode').
        columns (list): Columns to apply the strategy.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    if columns is None:
        columns = df.columns.tolist()
    if strategy == 'mean':
        df[columns] = df[columns].fillna(df[columns].mean())
    elif strategy == 'median':
        df[columns] = df[columns].fillna(df[columns].median())
    elif strategy == 'mode':
        df[columns] = df[columns].fillna(df[columns].mode().iloc[0])
    else:
        raise ValueError("Unsupported strategy. Choose 'mean', 'median', or 'mode'.")
    return df

def remove_outliers(df, column, method='IQR', multiplier=1.5):
    """
    Remove outliers from a specified column using the given method.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column (str): Column to remove outliers from.
        method (str): Method to use ('IQR').
        multiplier (float): Multiplier for determining outliers.

    Returns:
        pd.DataFrame: DataFrame without outliers.
    """
    if method == 'IQR':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        initial_count = df.shape[0]
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        removed = initial_count - df.shape[0]
        return df, removed
    else:
        raise ValueError("Unsupported method. Currently, only 'IQR' is supported.")

def scale_features(df, columns=None, method='standard'):
    """
    Scale specified numerical columns using the given method.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (list): Columns to scale.
        method (str): Scaling method ('standard', 'minmax', 'robust').

    Returns:
        pd.DataFrame: DataFrame with scaled features.
    """
    if columns is None:
        columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    scaler = None
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'robust':
        scaler = RobustScaler()
    else:
        raise ValueError("Unsupported scaling method. Choose 'standard', 'minmax', or 'robust'.")

    df[columns] = scaler.fit_transform(df[columns])
    return df