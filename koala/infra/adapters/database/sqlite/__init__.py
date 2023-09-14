# built-in
import logging
from typing import Union

# third-party
from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

# interfaces
from koala.infra.core.interfaces.database import IDatabase


class SQLite(IDatabase[Connection]):
    """Implements the IDatabase interface for SQLite databases.

    This class is responsible for managing SQLite database connections.

    Attributes:
        _connection_str: A string representing the SQLite database connection string.
        _engine: An Engine object for the SQLite database.
        _connection: A Connection object for the SQLite database.
        _session: A Session object for the SQLite database.
    """

    def __init__(self, connection_str: str) -> None:
        """Initializes SQLite with a given connection string.

        Args:
            connection_str: A string representing the SQLite database connection string.
        """
        self._connection_str = connection_str
        self._engine: Engine = create_engine(self._connection_str, echo=False)
        self._connection: Union[Connection, None] = None
        self._session: Union[None, Session] = None

    def __enter__(self):
        """Context manager enter method to connect to the database."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        """Context manager exit method to disconnect from the database."""
        self.disconnect()
    
    def connect(self) -> Union[Connection, None]:
        """Connects to the SQLite database.

        Returns:
            A Connection object or None if the connection fails.
        """
        if self._connection:
            return self._connection
        
        try:
            session = sessionmaker(self._engine)
            self._session = session()
            connection = self._engine.connect()
            self._connection = connection
            return connection
        except Exception as err:
            logging.error(f'Could not create database connection. {err}')
            return
    
    def disconnect(self) -> bool:
        """Disconnects from the SQLite database.

        Returns:
            A boolean indicating whether the disconnection was successful.
        """
        if not self._connection: return False

        try:
            self._connection.close()
            return True
        except Exception as err:
            logging.error(f'Could not disconnect from database. {err}')
            return False