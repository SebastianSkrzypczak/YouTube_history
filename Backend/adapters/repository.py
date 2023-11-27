from abc import ABC, abstractmethod
from sqlalchemy import Engine
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class AbstractRepository(ABC):
    @abstractmethod
    def read():
        ...

    @abstractmethod
    def write(self) -> None:
        pass


class SqlRepostory(AbstractRepository):
    """Class to handle SQL manipulation"""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def read(self, table_name: str) -> pd.DataFrame:
        """function reading data from SQL DB to Pandas DataFrame

        Args:
            table_name (str): name od an table in DB

        Returns:
            pd.DataFrame: Pandas DataFrame read from DB
        """
        try:
            df = pd.read_sql_table(table_name, self.engine)
        except ValueError as e:
            logger.error(e)
            raise
        return df

    def write(self, table_name: str, data: pd.DataFrame):
        """Function writing data to SQL DB

        Args:
            table_name (str): _description_
            data (pd.DataFrame): _description_
        """
        try:
            data.to_sql(table_name, self.engine, if_exists="replace", index=False)
        except ValueError as e:
            logger.error(e)
            raise
