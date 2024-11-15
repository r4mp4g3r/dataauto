# Usage Guide

This guide provides detailed instructions on how to use DataAuto to perform common data analysis tasks via the command-line interface.

## Table of Contents

	1.	Overview
	2.	Available Commands
	•	1. load
	•	2. summarize
	•	3. plot
	•	4. scatter (If Implemented)
	3.	Command Reference
	4.	Examples
	•	Basic Usage
	•	Advanced Usage
	5.	Error Handling
	6.	Best Practices
	7.	Help and Documentation

## Overview

DataAuto is a command-line tool designed to automate common data analysis tasks, making it easier for you to load, summarize, and visualize your data. Whether you’re a beginner looking to perform basic analyses or a seasoned data scientist seeking to streamline repetitive tasks, DataAuto offers the tools you need.

### Available Commands

DataAuto offers the following primary commands:
	1.	load: Load data from a CSV file.
	2.	summarize: Generate summary statistics of the data.
	3.	plot: Create visualizations for specified columns.
	4.	scatter: (Optional) Generate scatter plots for two specified columns.

Command Reference

1. load

Description: Import data from a CSV file into your analysis workflow.

Usage:
```bash
dataauto load <file_path>
```
Arguments:
	•	<file_path>: Path to the CSV file you want to load.

Example:
```bash
dataauto load examples/sample_data.csv
```
Expected Output:
```bash
Data loaded from examples/sample_data.csv. Shape: (10, 4)
```
2. summarize

Description: Generate and display summary statistics of the loaded data.

Usage:
```bash
dataauto summarize <file_path>
```
Arguments:
	•	<file_path>: Path to the CSV file you want to summarize.

Example:
```bash
dataauto summarize examples/sample_data.csv
```
Expected Output:
```bash
        Age  Salary
count  10.0    10.0
mean   32.3  65800.0
std     6.32711 16342.0
min    25.0  48000.0
25%    28.25 50000.0
50%    30.0  60000.0
75%    35.0  70000.0
max    45.0  90000.0
```
3. plot

Description: Generate and save a histogram with a Kernel Density Estimate (KDE) for a specified column.

Usage:
```bash
dataauto plot <file_path> --column <column_name>
```
Arguments:
	•	<file_path>: Path to the CSV file you want to plot.
	•	--column <column_name>: The name of the column you wish to visualize.

Example:
```bash
dataauto plot examples/sample_data.csv --column Age
```
Expected Output:
```bash
Plot saved for column: Age
```
Result:

A file named Age_distribution.png will be saved in your current directory, displaying a histogram with a KDE overlay for the “Age” column.

4. scatter (Optional)

Description: Generate and save a scatter plot for two specified columns.

Usage:
```bash
dataauto scatter <file_path> --column_x <column_x> --column_y <column_y>
```
Arguments:
	•	<file_path>: Path to the CSV file you want to plot.
	•	--column_x <column_x>: The name of the column for the x-axis.
	•	--column_y <column_y>: The name of the column for the y-axis.

Example:
```bash
dataauto scatter examples/sample_data.csv --column_x Age --column_y Salary
```
Expected Output:
```bash
Scatter plot saved as Age_vs_Salary_scatter.png
```
Result:

A file named Age_vs_Salary_scatter.png will be saved in your current directory, displaying a scatter plot of Age vs. Salary.

## Examples

### Basic Usage

Let’s walk through a basic workflow using the provided sample_data.csv.

Step 1: Load Data
```bash
dataauto load examples/sample_data.csv
```
Output:
```bash
Data loaded from examples/sample_data.csv. Shape: (10, 4)
```
Step 2: Summarize Data
```bash
dataauto summarize examples/sample_data.csv
```
Output:
```bash
        Age  Salary
count  10.0    10.0
mean   32.3  65800.0
std     6.32711 16342.0
min    25.0  48000.0
25%    28.25 50000.0
50%    30.0  60000.0
75%    35.0  70000.0
max    45.0  90000.0
```
Step 3: Plot Data
```bash
dataauto plot examples/sample_data.csv --column Age
```
Output:
```bash
Plot saved for column: Age
```
Verification:
	•	Locate Age_distribution.png in your current directory.
	•	Open the image to view the histogram with KDE.

Advanced Usage

Automating Multiple Tasks with a Shell Script

Create a shell script to automate loading, summarizing, and plotting data.
	1.	Create the Script:
```bash
touch run_analysis.sh
chmod +x run_analysis.sh
```

	2.	Edit run_analysis.sh:
```bash
#!/bin/bash

DATA_FILE="examples/sample_data.csv"

echo "Loading data..."
dataauto load $DATA_FILE

echo "Summarizing data..."
dataauto summarize $DATA_FILE

echo "Plotting data..."
dataauto plot $DATA_FILE --column Age

echo "Analysis complete."
```

	3.	Run the Script:
```bash
./run_analysis.sh
```


Expected Output:
```bash
Loading data...
Data loaded from examples/sample_data.csv. Shape: (10, 4)
Summarizing data...
        Age  Salary
count  10.0    10.0
mean   32.3  65800.0
std     6.32711 16342.0
min    25.0  48000.0
25%    28.25 50000.0
50%    30.0  60000.0
75%    35.0  70000.0
max    45.0  90000.0
Plotting data...
Plot saved for column: Age
Analysis complete.
```
## Error Handling

DataAuto provides meaningful error messages to help you troubleshoot issues.

Common Errors

	1.	File Not Found
Error Message:
```bash
Error: The file 'path/to/file.csv' does not exist.
```
Solution: Verify the file path and ensure the file exists.

	2.	Invalid Column Name
Error Message:
```bash
Error: Column 'InvalidColumn' does not exist in the data.
```
Solution: Check the column names in your CSV file and provide a valid column name.

	3.	Malformed CSV File
Error Message:
```bash
Error: Failed to load data: ParserError: Error tokenizing data. C error: Expected X fields in line Y, saw Z
```
Solution: Ensure your CSV file is properly formatted and free of errors.

	4.	Missing Dependencies
Error Message:
```bash
ModuleNotFoundError: No module named 'pandas'
```
Solution: Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
Best Practices

	•	Consistent File Paths: Always provide the correct path to your CSV files to avoid errors.
	•	Valid Column Names: Ensure that the column names you specify for plotting exist in your dataset.
	•	Data Quality: Clean your data before analysis to obtain accurate summaries and visualizations.
	•	Use Virtual Environments: To manage dependencies and avoid conflicts, use virtual environments.
	•	Regularly Update Dependencies: Keep your packages up-to-date to benefit from the latest features and security patches.

Help and Documentation

For detailed information about each command and its options, use the --help flag.

Command-Level Help

	•	General Help
```bash
dataauto --help
```
Output:
```bash
Usage: dataauto [OPTIONS] COMMAND [ARGS]...

  DataAuto: Automate your data analysis tasks with ease.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  load      Load data from a CSV file.
  plot      Generate a plot for a specified column.
  scatter   Generate a scatter plot for two specified columns.
  summarize Generate summary statistics of the data.
```

	•	Specific Command Help
```bash
dataauto summarize --help
```
Output:
```bash
Usage: dataauto summarize [OPTIONS] FILE_PATH

  Provide summary statistics of the data.

Arguments:
  FILE_PATH  Path to the CSV file.

Options:
  --help  Show this message and exit.
```


### Accessing Full Documentation

For comprehensive guides and tutorials, refer to the Documentation section.