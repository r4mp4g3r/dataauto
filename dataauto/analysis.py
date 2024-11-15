# dataauto/analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Failed to load data: {e}")

def summarize_data(data):
    """
    Generate summary statistics of the DataFrame.

    Parameters:
        data (pd.DataFrame): Data to summarize.

    Returns:
        str: Summary statistics as a string.
    """
    try:
        summary = data.describe(include='all').to_string()
        return summary
    except Exception as e:
        raise ValueError(f"Failed to summarize data: {e}")

def plot_data(data, column, save_dir='.'):
    """
    Generate and save a histogram with KDE for a specified column.

    Parameters:
        data (pd.DataFrame): Data to plot.
        column (str): Column name to plot.

    Returns:
        None
    """
    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist in the data.")

    try:
        plt.figure(figsize=(10, 6))
        sns.histplot(data[column].dropna(), kde=True)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.savefig(f'{save_dir}/{column}_distribution.png')
        plt.close()
    except Exception as e:
        raise ValueError(f"Failed to plot data: {e}")

def plot_scatter(data, column_x, column_y, save_dir='.'):
    """
    Generate and save a scatter plot for two specified columns.

    Parameters:
        data (pd.DataFrame): Data to plot.
        column_x (str): Column name for the x-axis.
        column_y (str): Column name for the y-axis.

    Returns:
        None
    """
    if column_x not in data.columns or column_y not in data.columns:
        raise ValueError(f"One or both columns '{column_x}', '{column_y}' do not exist in the data.")

    try:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=data, x=column_x, y=column_y)
        plt.title(f'Scatter Plot of {column_x} vs {column_y}')
        plt.xlabel(column_x)
        plt.ylabel(column_y)
        plt.savefig(f'{save_dir}/{column_x}_vs_{column_y}_scatter.png')
        plt.close()
    except Exception as e:
        raise ValueError(f"Failed to plot scatter data: {e}")