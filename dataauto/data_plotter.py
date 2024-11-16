# dataauto/data_plotter.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
import sys

def plot_histogram(df, column, output_dir='plots', interactive=False):
    """
    Generate a histogram for a specified column.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column (str): The column for which to plot the histogram.
        output_dir (str): Directory to save the plots.
        interactive (bool): Whether to generate an interactive plot.

    Returns:
        None
    """
    try:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise TypeError(f"Column '{column}' is not numerical.")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Static Histogram
        plt.figure(figsize=(8, 6))
        sns.histplot(df[column], kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{column}_histogram.png"))
        plt.close()
        print(f"Histogram for {column} saved to {output_dir}/{column}_histogram.png.")

        # Interactive Histogram
        if interactive:
            fig = px.histogram(df, x=column, nbins=30, title=f'Interactive Histogram of {column}')
            fig.write_html(os.path.join(output_dir, f"{column}_histogram.html"))
            print(f"Interactive histogram for {column} saved to {output_dir}/{column}_histogram.html.")

    except Exception as e:
        print(f"Error during plotting: {e}")
        sys.exit(1)

def plot_scatter(df, x, y, output_dir='plots', interactive=False):
    """
    Generate a scatter plot for specified x and y columns.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        x (str): The column for the x-axis.
        y (str): The column for the y-axis.
        output_dir (str): Directory to save the plots.
        interactive (bool): Whether to generate an interactive plot.

    Returns:
        None
    """
    try:
        if x not in df.columns or y not in df.columns:
            raise ValueError("Specified x or y column does not exist in the DataFrame.")
        if not (pd.api.types.is_numeric_dtype(df[x]) and pd.api.types.is_numeric_dtype(df[y])):
            raise TypeError("Both x and y columns must be numerical.")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Static Scatter Plot
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x=x, y=y)
        plt.title(f'Scatter Plot of {x} vs {y}')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{x}_vs_{y}_scatter.png"))
        plt.close()
        print(f"Scatter plot for {x} vs {y} saved to {output_dir}/{x}_vs_{y}_scatter.png.")

        # Interactive Scatter Plot
        if interactive:
            fig = px.scatter(df, x=x, y=y, title=f'Interactive Scatter Plot of {x} vs {y}')
            fig.write_html(os.path.join(output_dir, f"{x}_vs_{y}_scatter.html"))
            print(f"Interactive scatter plot saved to {output_dir}/{x}_vs_{y}_scatter.html.")

    except Exception as e:
        print(f"Error during plotting: {e}")
        sys.exit(1)

def plot_box(df, column, output_dir='plots', interactive=False):
    """
    Generate a box plot for a specified column.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column (str): The column for which to plot the box plot.
        output_dir (str): Directory to save the plots.
        interactive (bool): Whether to generate an interactive plot.

    Returns:
        None
    """
    try:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise TypeError(f"Column '{column}' is not numerical.")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Static Box Plot
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=df[column])
        plt.title(f'Box Plot of {column}')
        plt.xlabel(column)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{column}_boxplot.png"))
        plt.close()
        print(f"Box plot for {column} saved to {output_dir}/{column}_boxplot.png.")

        # Interactive Box Plot
        if interactive:
            fig = px.box(df, y=column, title=f'Interactive Box Plot of {column}')
            fig.write_html(os.path.join(output_dir, f"{column}_boxplot.html"))
            print(f"Interactive box plot saved to {output_dir}/{column}_boxplot.html.")

    except Exception as e:
        print(f"Error during plotting: {e}")
        sys.exit(1)

def plot_heatmap(df, columns, output_dir='plots', interactive=False):
    """
    Generate a heatmap for specified columns.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (list): List of columns to include in the heatmap.
        output_dir (str): Directory to save the plots.
        interactive (bool): Whether to generate an interactive plot.

    Returns:
        None
    """
    try:
        for column in columns:
            if column not in df.columns:
                raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
            if not pd.api.types.is_numeric_dtype(df[column]):
                raise TypeError(f"Column '{column}' is not numerical.")

        if len(columns) < 2:
            raise ValueError("At least two columns are required to generate a heatmap.")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        corr = df[columns].corr()

        # Static Heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"))
        plt.close()
        print(f"Correlation heatmap saved to {output_dir}/correlation_heatmap.png.")

        # Interactive Heatmap
        if interactive:
            fig = px.imshow(corr, text_auto=True, aspect="auto", title="Interactive Correlation Heatmap")
            fig.write_html(os.path.join(output_dir, "correlation_heatmap.html"))
            print(f"Interactive correlation heatmap saved to {output_dir}/correlation_heatmap.html.")

    except Exception as e:
        print(f"Error during plotting: {e}")
        sys.exit(1)

def plot_line(df, x, y, output_dir='plots', interactive=False):
    """
    Generate a line plot for specified x and y columns.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        x (str): The column for the x-axis.
        y (str): The column for the y-axis.
        output_dir (str): Directory to save the plots.
        interactive (bool): Whether to generate an interactive plot.

    Returns:
        None
    """
    try:
        if x not in df.columns or y not in df.columns:
            raise ValueError("Specified x or y column does not exist in the DataFrame.")
        if not (pd.api.types.is_numeric_dtype(df[x]) and pd.api.types.is_numeric_dtype(df[y])):
            raise TypeError("Both x and y columns must be numerical.")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Static Line Plot
        plt.figure(figsize=(8, 6))
        sns.lineplot(data=df, x=x, y=y)
        plt.title(f'Line Plot of {y} over {x}')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{y}_over_{x}_line.png"))
        plt.close()
        print(f"Line plot for {y} over {x} saved to {output_dir}/{y}_over_{x}_line.png.")

        # Interactive Line Plot
        if interactive:
            fig = px.line(df, x=x, y=y, title=f'Interactive Line Plot of {y} over {x}')
            fig.write_html(os.path.join(output_dir, f"{y}_over_{x}_line.html"))
            print(f"Interactive line plot saved to {output_dir}/{y}_over_{x}_line.html.")

    except Exception as e:
        print(f"Error during plotting: {e}")
        sys.exit(1)