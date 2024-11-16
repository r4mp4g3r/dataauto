import pandas as pd

# Define the data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 40, 45],
    'Salary': [70000, 80000, 90000, 100000, 110000],
    'Department': ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel with sheet name 'Sheet1'
df.to_excel('sample_data.xlsx', sheet_name='Sheet1', index=False)