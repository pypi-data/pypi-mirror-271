import sqlite3
from typing import Any, List, Tuple

def create_table(conn: sqlite3.Connection, table_name: str, columns: dict):
    """
    Creates a table with the given name and columns.
    :param conn: Database connection
    :param table_name: Name of the table to create
    :param columns: A dictionary of column names and their SQL types
    """
    cols = ', '.join([f"{name} {type}" for name, type in columns.items()])
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols});"
    conn.execute(sql)
    conn.commit()

def add_data(conn: sqlite3.Connection, table_name: str, data: List[Tuple[Any]]):
    """
    Adds data to the given table.
    :param conn: Database connection
    :param table_name: Name of the table to insert data
    :param data: List of tuples representing the rows to be inserted
    """
    placeholders = ', '.join(['?' for _ in data[0]])
    sql = f"INSERT INTO {table_name} VALUES ({placeholders});"
    conn.executemany(sql, data)
    conn.commit()

def query_data(conn: sqlite3.Connection, table_name: str, conditions: str = "", columns: List[str] = ["*"], order_by: str = ""):
    """
    Queries data from the table.
    :param conn: Database connection
    :param table_name: Name of the table to query
    :param conditions: Conditions for filtering (WHERE clause)
    :param columns: List of column names to fetch
    :param order_by: Column to order the results
    """
    select_cols = ', '.join(columns)
    sql = f"SELECT {select_cols} FROM {table_name}"
    if conditions:
        sql += f" WHERE {conditions}"
    if order_by:
        sql += f" ORDER BY {order_by}"
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def delete_table(conn: sqlite3.Connection, table_name: str):
    """
    Deletes the specified table from the database.
    :param conn: Database connection
    :param table_name: Name of the table to be deleted
    """
    sql = f"DROP TABLE IF EXISTS {table_name};"
    conn.execute(sql)
    conn.commit()