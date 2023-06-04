import pyarrow  as pa
from typing import Union
from dryg.settings import DB_URI

import lancedb

def connection() -> lancedb.LanceDBConnection:
    """
    Connect to the database

    Returns:
        lancedb.LanceDBConnection: LanceDBConnection object
    """
    db = lancedb.connect(DB_URI)
    return db

def open_table(table_name: str) -> Union[lancedb.LanceDBConnection, None]:
    """
    Open a table from the database

    Args:
        table_name (str): Name of the table

    Returns:
        lancedb.LanceDBConnection: LanceDBConnection object
    """
    db = connection()
    try:
        table = db.open_table(table_name) if table_name in db.table_names() else None
        return table
    except ValueError:
        return None

def create_table(table_name: str, table: pa.Table, mode: str = "overwrite") -> lancedb.LanceDBConnection:
    """
    Create a table in the database

    Args:
        table_name (str): Name of the table
        table (pa.Table): Table to be created
        mode (str, optional): Mode to use when creating the table. Defaults to "overwrite".

    Returns:
        lancedb.LanceDBConnection: LanceDBConnection object
    """
    db = connection()
    db.create_table(table_name, table, mode=mode)
    return db
    
    