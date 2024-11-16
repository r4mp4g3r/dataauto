# dataauto/data_saver.py

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def save_csv(df, output_file):
    """Save DataFrame to a CSV file."""
    try:
        df.to_csv(output_file, index=False)
    except Exception as e:
        raise e

def save_json(df, output_file):
    """Save DataFrame to a JSON file."""
    try:
        df.to_json(output_file, orient='records', lines=True)
    except Exception as e:
        raise e

def save_excel(df, output_file, sheet_name='Sheet1'):
    """Save DataFrame to an Excel file."""
    try:
        df.to_excel(output_file, index=False, sheet_name=sheet_name)
    except Exception as e:
        raise e

def save_sql(df, db_type, host, port, dbname, user, password, query):
    """Save DataFrame to a SQL database."""
    try:
        if db_type.lower() == 'postgresql':
            engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
        elif db_type.lower() == 'mysql':
            engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}')
        else:
            raise ValueError("Unsupported database type. Choose 'postgresql' or 'mysql'.")
        
        df.to_sql(name='data_table', con=engine, if_exists='replace', index=False)
    except SQLAlchemyError as e:
        raise e
    except Exception as e:
        raise e