from typing import List

from .exceptions import IncompleteQueryError

class QueryBuilder:
    def __init__(self):
        """
        Initializes the QueryBuilder.
        """
        self._select = None
        self._from = None
        self._where = ""
        self._limit = None

    def select(self, columns: List[str]) -> 'QueryBuilder':
        """
        Specifies the columns to select from the table.
        
        :param columns: A list of column names to include in the select clause.
        :return: Instance of QueryBuilder.
        """
        if not columns:
            raise ValueError("Column list must not be empty.")
        self._select = ", ".join(columns)
        return self

    def from_table(self, table_name: str) -> 'QueryBuilder':
        """
        Specifies the table to select from.
        
        :param table_name: Name of the table.
        :return: Instance of QueryBuilder.
        """
        if not table_name:
            raise ValueError("Table name must not be empty.")
        self._from = f"FROM {table_name}"
        return self

    def where(self, condition: str) -> 'QueryBuilder':
        """
        Adds a condition to the query.
        
        :param condition: Condition string.
        :return: Instance of QueryBuilder.
        """
        self._where = f"WHERE {condition}"
        return self

    def limit(self, limit: int) -> 'QueryBuilder':
        """
        Adds a limit to the number of results returned.
        
        :param limit: The maximum number of results to return.
        :return: Instance of QueryBuilder.
        """
        if limit < 1:
            raise ValueError("Limit must be at least 1.")
        self._limit = f"LIMIT {limit}"
        return self

    def build(self) -> str:
        """
        Builds and returns the SQL query string.
        
        :return: The constructed SQL query string.
        """
        if self._select is None or self._from is None:
            raise IncompleteQueryError("Select or From clause missing.")
        query = f"SELECT {self._select} {self._from}"
        if self._where:
            query += f" {self._where}"
        if self._limit:
            query += f" {self._limit}"
        return query