# dataauto/preprocessing.py

import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from scipy import stats
import numpy as np

def fill_missing(df, strategy='mean', columns=None, value=None):
    """
    Fill missing values in specified columns using the given strategy.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        strategy (str): Strategy to use ('mean', 'median', 'mode', 'constant').
        columns (list): List of columns to fill missing values. If None, all columns are used.
        value (any): The constant value to use if strategy is 'constant'.

    Returns:
        pd.DataFrame: DataFrame with missing values filled.
    """
    if columns is None:
        columns = df.columns.tolist()

    for column in columns:
        if column not in df.columns:
            print(f"Warning: Column '{column}' does not exist in the DataFrame. Skipping.")
            continue

        if df[column].dtype in ['object', 'category']:
            if strategy == 'mode':
                df[column] = df[column].fillna(df[column].mode()[0])
            elif strategy == 'constant' and value is not None:
                df[column] = df[column].fillna(value)
            else:
                print(f"Warning: Strategy '{strategy}' not supported for non-numerical column '{column}'. Skipping.")
        else:
            if strategy == 'mean':
                df[column] = df[column].fillna(df[column].mean())
            elif strategy == 'median':
                df[column] = df[column].fillna(df[column].median())
            elif strategy == 'mode':
                df[column] = df[column].fillna(df[column].mode()[0])
            elif strategy == 'constant':
                if value is not None:
                    df[column] = df[column].fillna(value)
                else:
                    raise ValueError("Value must be provided for constant strategy.")
            else:
                raise ValueError(f"Unsupported strategy '{strategy}'. Choose from 'mean', 'median', 'mode', 'constant'.")

    return df

def remove_outliers(df, column, method='IQR', multiplier=1.5):
    """
    Remove outliers from a specified column using the chosen method.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column (str): The column from which to remove outliers.
        method (str): The method to use ('IQR' or 'Z-score').
        multiplier (float): The multiplier for determining outlier thresholds.

    Returns:
        pd.DataFrame: The DataFrame with outliers removed.
        int: Number of outliers removed.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise TypeError(f"Column '{column}' is not numerical.")

    initial_count = df.shape[0]

    if method == 'IQR':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    elif method == 'Z-score':
        z_scores = stats.zscore(df[column].dropna())
        abs_z_scores = np.abs(z_scores)
        filter_mask = abs_z_scores < multiplier
        df_filtered = df.iloc[filter_mask.nonzero()[0]]
    else:
        raise ValueError("Unsupported method. Choose 'IQR' or 'Z-score'.")

    removed = initial_count - df_filtered.shape[0]
    return df_filtered, removed

def scale_data(df, columns, method='standard'):
    """
    Scale specified numerical columns using the given method.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (list): List of columns to scale.
        method (str): Scaling method ('standard' or 'minmax').

    Returns:
        pd.DataFrame: DataFrame with scaled columns.
    """
    if not columns:
        raise ValueError("No columns specified for scaling.")

    scaler = None
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    else:
        raise ValueError("Unsupported scaling method. Choose 'standard' or 'minmax'.")

    for column in columns:
        if column not in df.columns:
            print(f"Warning: Column '{column}' does not exist in the DataFrame. Skipping.")
            continue

        if not pd.api.types.is_numeric_dtype(df[column]):
            print(f"Warning: Column '{column}' is not numerical. Skipping.")
            continue

        df[column] = scaler.fit_transform(df[[column]])

    return df

def preprocess_features(X):
    """
    Preprocess features by encoding categorical variables and scaling numerical variables.

    Parameters:
        X (pd.DataFrame): Feature DataFrame.

    Returns:
        ColumnTransformer: A scikit-learn ColumnTransformer object for preprocessing.
    """
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['float64', 'int64']).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ]
    )

    return preprocessor