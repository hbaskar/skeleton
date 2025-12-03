import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()

SQL_DRIVER = os.getenv('AZURE_SQL_DRIVER', 'ODBC Driver 18 for SQL Server')
SQL_PORT = os.getenv('AZURE_SQL_PORT', '1433')
SQL_SERVER = os.getenv('AZURE_SQL_SERVER')
SQL_DATABASE = os.getenv('AZURE_SQL_DATABASE')
SQL_USERNAME = os.getenv('AZURE_SQL_USERNAME')
SQL_PASSWORD = os.getenv('AZURE_SQL_PASSWORD')
SQL_AUTHENTICATION = os.getenv('AZURE_SQL_AUTHENTICATION', 'ActiveDirectoryPassword')

# Enable pyodbc connection pooling (enabled by default, but can be configured)
pyodbc.pooling = True

def get_connection_string():
    if SQL_AUTHENTICATION == 'ActiveDirectoryPassword':
        return (
            f"Driver={{{SQL_DRIVER}}};"
            f"Server={SQL_SERVER},{SQL_PORT};"
            f"Database={SQL_DATABASE};"
            f"Authentication=ActiveDirectoryPassword;"
            f"Uid={SQL_USERNAME};"
            f"Pwd={SQL_PASSWORD};"
        )
    elif SQL_AUTHENTICATION == 'ActiveDirectoryMsi':
        return (
            f"Driver={{{SQL_DRIVER}}};"
            f"Server={SQL_SERVER},{SQL_PORT};"
            f"Database={SQL_DATABASE};"
            f"Authentication=ActiveDirectoryMsi;"
        )
    else:
        raise ValueError('Unsupported AZURE_SQL_AUTHENTICATION value')

def get_db_connection():
    """
    Returns a pooled pyodbc connection using the current config.
    """
    conn_str = get_connection_string()
    return pyodbc.connect(conn_str, autocommit=True)
