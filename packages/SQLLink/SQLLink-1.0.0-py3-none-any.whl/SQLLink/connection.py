import sqlite3
from sqlite3 import Connection, Cursor
from typing import Optional

from .exceptions import DatabaseConnectionError

class DatabaseConnection:
    def __init__(self, db_file: str):
        """
        Initializes a new database connection.
        
        :param db_file: Path to the SQLite database file.
        """
        self.db_file: str = db_file
        self.conn: Optional[Connection] = None

    def create_connection(self) -> Connection:
        """
        Create a database connection to the SQLite database specified by db_file.
        
        :return: A SQLite connection object.
        :raises DatabaseConnectionError: If the connection to the database fails.
        """
        try:
            self.conn = sqlite3.connect(self.db_file)
            return self.conn
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Failed to connect to database: {e}")

    def close_connection(self) -> None:
        """
        Close the database connection.
        """
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, query: str) -> Cursor:
        """
        Execute a SQL query using the active database connection.
        
        :param query: SQL query string to be executed.
        :return: Cursor object containing the query results.
        :raises DatabaseConnectionError: If query execution fails.
        """
        if self.conn is None:
            raise DatabaseConnectionError("No database connection is open.")
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            return cursor
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Error executing query: {e}")

    def __enter__(self) -> Connection:
        """
        Enable use of 'with' statements to manage resources.
        
        :return: A SQLite connection object.
        """
        return self.create_connection()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Ensure the connection closes after the 'with' block.
        """
        self.close_connection()
