class DatabaseConnectionError(Exception):
    """Exception raised for errors that occur during connection to the database."""
    def __init__(self, message="Failed to connect to the database"):
        self.message = message
        super().__init__(self.message)

class QueryError(Exception):
    """Exception raised for errors that occur during SQL query execution."""
    def __init__(self, message="Error executing SQL query"):
        self.message = message
        super().__init__(self.message)

class ConfigurationError(Exception):
    """Exception raised for errors related to configuration settings of the database."""
    def __init__(self, message="Configuration error in database settings"):
        self.message = message
        super().__init__(self.message)

class IncompleteQueryError(QueryError):
    """Exception raised when trying to build an incomplete query."""
    pass

class InvalidInputError(Exception):
    """Exception raised for invalid input errors in query parameters."""
    def __init__(self, message="Invalid input provided"):
        self.message = message
        super().__init__(self.message)
