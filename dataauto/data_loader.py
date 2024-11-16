# dataauto/data_loader.py

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def load_csv(file_path):
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise e

def load_json(file_path):
    """Load data from a JSON file."""
    try:
        df = pd.read_json(file_path, lines=True)
        return df
    except Exception as e:
        raise e

def load_excel(file_path, sheet_name=0):
    """Load data from an Excel file."""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        raise e

def load_sql(db_type, host, port, dbname, user, password, query):
    """Load data from a SQL database."""
    try:
        if db_type.lower() == 'postgresql':
            engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
        elif db_type.lower() == 'mysql':
            engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}')
        else:
            raise ValueError("Unsupported database type. Choose 'postgresql' or 'mysql'.")
    
        with engine.connect() as connection:
            df = pd.read_sql_query(query, connection)
        return df
    except SQLAlchemyError as e:
        raise e
    except Exception as e:
        raise e