# dataauto/cli.py

import click
import pandas as pd
from dataauto.data_loader import load_csv, load_json, load_excel, load_sql
from dataauto.data_saver import save_csv, save_json, save_excel, save_sql
from dataauto.data_cleaner import clean_data, remove_outliers, scale_features
from dataauto.data_plotter import plot_histogram, plot_scatter, plot_box, plot_heatmap, plot_line
from dataauto.model_trainer import train_model
from dataauto.report_generator import generate_report
from dataauto.scheduler import schedule_command
from dataauto import __version__
import os
import joblib

@click.group()
@click.version_option(version=__version__, prog_name='DataAuto')
def cli():
    """DataAuto: Automate your data analysis tasks with ease."""
    pass

@cli.command()
@click.argument('file_path')
@click.option('--format', type=click.Choice(['csv', 'json', 'excel', 'sql']), default='csv', help='Format of the input file')
@click.option('--db-type', type=click.Choice(['postgresql', 'mysql']), help='Type of the SQL database')
@click.option('--host', help='Database host')
@click.option('--port', type=int, help='Database port')
@click.option('--dbname', help='Database name')
@click.option('--user', help='Database user')
@click.option('--password', help='Database password')
@click.option('--query', help='SQL query to execute')
@click.option('--sheet', default='Sheet1', help='Sheet name or index for Excel files')
def load(file_path, format, db_type, host, port, dbname, user, password, query, sheet):
    """Load data from a specified file format or SQL database."""
    try:
        if format == 'csv':
            df = load_csv(file_path)
        elif format == 'json':
            df = load_json(file_path)
        elif format == 'excel':
            df = load_excel(file_path, sheet_name=sheet)
        elif format == 'sql':
            if not all([db_type, host, port, dbname, user, password, query]):
                raise click.ClickException("All SQL connection parameters must be provided for SQL format.")
            df = load_sql(db_type, host, port, dbname, user, password, query)
        click.echo(f"Data loaded from {file_path}. Shape: {df.shape}")
    except Exception as e:
        raise click.ClickException(f"Error loading data: {e}")

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--format', type=click.Choice(['csv', 'json', 'excel', 'sql']), default='csv', help='Format to save the data')
@click.option('--db-type', type=click.Choice(['postgresql', 'mysql']), help='Type of the SQL database for saving to SQL')
@click.option('--host', help='Database host')
@click.option('--port', type=int, help='Database port')
@click.option('--dbname', help='Database name')
@click.option('--user', help='Database user')
@click.option('--password', help='Database password')
@click.option('--query', help='SQL query to save the data to')
@click.option('--sheet', default='Sheet1', help='Sheet name for Excel files')
def save(input_file, output_file, format, db_type, host, port, dbname, user, password, query, sheet):
    """Save data to a specified file format or SQL database."""
    try:
        df = pd.read_csv(input_file)
        if format == 'csv':
            save_csv(df, output_file)
        elif format == 'json':
            save_json(df, output_file)
        elif format == 'excel':
            save_excel(df, output_file, sheet_name=sheet)
        elif format == 'sql':
            if not all([db_type, host, port, dbname, user, password, query]):
                raise click.ClickException("All SQL connection parameters must be provided for SQL format.")
            save_sql(df, db_type, host, port, dbname, user, password, query)
        click.echo(f"Data saved successfully to {output_file} in {format.upper()} format.")
    except Exception as e:
        raise click.ClickException(f"Error saving data: {e}")

@cli.command()
@click.argument('file_path')
@click.option('--strategy', type=click.Choice(['mean', 'median', 'mode']), default='mean', help='Strategy to fill missing values')
@click.option('--columns', multiple=True, required=True, help='Columns to clean')
@click.option('--output-file', required=True, help='Path to save the cleaned data')
def clean(file_path, strategy, columns, output_file):
    """Clean data by handling missing values."""
    try:
        df = pd.read_csv(file_path)
        df_cleaned = clean_data(df, strategy=strategy, columns=list(columns))
        df_cleaned.to_csv(output_file, index=False)
        click.echo(f"Missing values filled using {strategy} strategy for columns: {', '.join(columns)}.")
        click.echo(f"Cleaned data saved to {output_file}.")
    except Exception as e:
        raise click.ClickException(f"Error cleaning data: {e}")

@cli.command()
@click.argument('file_path')
@click.option('--column', required=True, help='Column to remove outliers from')
@click.option('--method', type=click.Choice(['IQR']), default='IQR', help='Method to remove outliers')
@click.option('--multiplier', type=float, default=1.5, help='Multiplier for determining outliers')
@click.option('--output-file', required=True, help='Path to save the data without outliers')
def remove_outlier(file_path, column, method, multiplier, output_file):
    """Remove outliers from a specified column."""
    try:
        df = pd.read_csv(file_path)
        df_cleaned, removed = remove_outliers(df, column=column, method=method, multiplier=multiplier)
        df_cleaned.to_csv(output_file, index=False)
        click.echo(f"Removed {removed} outliers from column '{column}' using {method} method.")
        click.echo(f"Cleaned data saved to {output_file}.")
    except Exception as e:
        raise click.ClickException(f"Error removing outliers: {e}")

@cli.command()
@click.argument('file_path')
@click.option('--columns', multiple=True, required=True, help='Columns to scale')
@click.option('--method', type=click.Choice(['standard', 'minmax', 'robust']), default='standard', help='Scaling method')
@click.option('--output-file', required=True, help='Path to save the scaled data')
def scale(file_path, columns, method, output_file):
    """Scale numerical features."""
    try:
        df = pd.read_csv(file_path)
        df_scaled = scale_features(df, columns=list(columns), method=method)
        df_scaled.to_csv(output_file, index=False)
        click.echo(f"Columns {', '.join(columns)} scaled using {method} method.")
        click.echo(f"Scaled data saved to {output_file}.")
    except Exception as e:
        raise click.ClickException(f"Error scaling data: {e}")

@cli.command()
@click.argument('file_path')
@click.option('--plot-type', type=click.Choice(['histogram', 'scatter', 'box', 'heatmap', 'line']), required=True, help='Type of plot to generate')
@click.option('--columns', multiple=True, help='Columns to plot (for histogram, box, heatmap)')
@click.option('--x', help='X-axis column (for scatter and line plots)')
@click.option('--y', help='Y-axis column (for scatter and line plots)')
@click.option('--output-dir', required=True, help='Directory to save plots')
@click.option('--interactive', is_flag=True, help='Generate interactive plots')
def plot(file_path, plot_type, columns, x, y, output_dir, interactive):
    """Generate plots from the data."""
    try:
        df = pd.read_csv(file_path)
        os.makedirs(output_dir, exist_ok=True)
        if plot_type == 'histogram':
            if not columns:
                raise click.ClickException("Please specify at least one column for histogram.")
            for col in columns:
                plot_histogram(df, col, output_dir, interactive=interactive)
        elif plot_type == 'scatter':
            if not all([x, y]):
                raise click.ClickException("Please specify both --x and --y columns for scatter plot.")
            plot_scatter(df, x, y, output_dir, interactive=interactive)
        elif plot_type == 'box':
            if not columns:
                raise click.ClickException("Please specify at least one column for box plot.")
            for col in columns:
                plot_box(df, col, output_dir, interactive=interactive)
        elif plot_type == 'heatmap':
            plot_heatmap(df, output_dir, interactive=interactive)
        elif plot_type == 'line':
            if not all([x, y]):
                raise click.ClickException("Please specify both --x and --y columns for line plot.")
            plot_line(df, x, y, output_dir, interactive=interactive)
        click.echo(f"{plot_type.capitalize()} plots saved to {output_dir}.")
    except Exception as e:
        raise click.ClickException(f"Error generating plots: {e}")

@cli.command()
@click.argument('file_path')
@click.option('--target', required=True, help='Target column for modeling')
@click.option('--model-type', type=click.Choice(['regressor', 'classifier']), required=True, help='Type of model to train')
@click.option('--test-size', type=float, default=0.2, help='Proportion of data to use as test set')
@click.option('--random-state', type=int, default=42, help='Random state for reproducibility')
@click.option('--output-model', required=True, help='Path to save the trained model')
@click.option('--output-report', required=True, help='Path to save the model report')
def train(file_path, target, model_type, test_size, random_state, output_model, output_report):
    """Train a machine learning model."""
    try:
        df = pd.read_csv(file_path)
        model, report = train_model(df, target=target, model_type=model_type, test_size=test_size, random_state=random_state)
        joblib.dump(model, output_model)
        with open(output_report, 'w') as f:
            f.write(report)
        click.echo("Model trained successfully.")
        click.echo(report)
        click.echo(f"Trained model saved to {output_model}.")
        click.echo(f"Model report saved to {output_report}.")
    except Exception as e:
        raise click.ClickException(f"Error training model: {e}")

@cli.command()
@click.argument('file_path')
@click.option('--schedule', required=True, help='Schedule time in 24-hour format HH:MM (e.g., "14:30")')
@click.option('--command', required=True, type=click.Choice(['load', 'save', 'clean', 'scale', 'plot', 'train']), help='Command to schedule')
def schedule(file_path, schedule, command):
    """Schedule a CLI command."""
    try:
        schedule_command(command, file_path, schedule)
        click.echo(f"Scheduled command '{command}' on file '{file_path}' at '{schedule}'.")
    except Exception as e:
        raise click.ClickException(f"Error scheduling command: {e}")

if __name__ == '__main__':
    cli()