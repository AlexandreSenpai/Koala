import logging
from typing import Union
from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from koala.infra.core.interfaces.database import IDatabase


class SQLite(IDatabase[Connection]):
    def __init__(self, connection_str: str) -> None:
        self._connection_str = connection_str
        self._engine: Engine = create_engine(self._connection_str, echo=False)
        self._connection: Union[Connection, None] = None
        self._session: Union[None, Session] = None

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.disconnect()
    
    def connect(self) -> Union[Connection, None]:
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
        if not self._connection: return False

        try:
            self._connection.close()
            return True
        except Exception as err:
            logging.error(f'Could not disconnect from database. {err}')
            return False