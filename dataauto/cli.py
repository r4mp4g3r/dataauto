# dataauto/cli.py
import click
from dataauto.analysis import load_data, summarize_data, plot_data, plot_scatter
from dataauto import __version__

@click.group()
@click.version_option(version=__version__, prog_name='DataAuto')
def cli():
    """DataAuto: Automate your data analysis tasks with ease."""
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def load(file_path):
    """Load data from a CSV file."""
    data = load_data(file_path)
    click.echo(f'Data loaded from {file_path}. Shape: {data.shape}')

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def summarize(file_path):
    """Provide summary statistics of the data."""
    data = load_data(file_path)
    summary = summarize_data(data)
    click.echo(summary)

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--column', prompt='Column to plot', help='Column name to plot.')
@click.option('--output-dir', default='.', help='Directory to save the plot.')
def plot(file_path, column, output_dir):
    """Generate a plot for a specified column."""
    data = load_data(file_path)
    try:
        plot_data(data, column, save_dir=output_dir)
        click.echo(f'Plot saved for column: {column} in {output_dir}')
    except Exception as e:
        click.echo(f'Error generating plot: {e}')

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--column_x', prompt='X-axis column', help='Column name for the x-axis.')
@click.option('--column_y', prompt='Y-axis column', help='Column name for the y-axis.')
@click.option('--output-dir', default='.', help='Directory to save the scatter plot.')
def scatter(file_path, column_x, column_y, output_dir):
    """Generate a scatter plot for two specified columns."""
    data = load_data(file_path)
    try:
        plot_scatter(data, column_x, column_y, save_dir=output_dir)
        click.echo(f'Scatter plot saved as {column_x}_vs_{column_y}_scatter.png in {output_dir}')
    except Exception as e:
        click.echo(f'Error generating scatter plot: {e}')

if __name__ == '__main__':
    cli()