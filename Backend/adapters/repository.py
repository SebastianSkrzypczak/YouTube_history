from abc import ABC, abstractmethod
import pandas as pd


class AbstractRepository(ABC):

    @abstractmethod
    def read():
        ...

    @abstractmethod
    def write(self) -> None:
        pass


class SqlRepostory(AbstractRepository):
    '''Class to handle SQL manipulation'''

    def __init__(self, engine) -> None:
        self.engine = engine

    def read(self, table_name: str) -> pd.DataFrame:
        """function reading data from SQL DB to Pandas DataFrame

        Args:
            table_name (str): name od an table in DB

        Returns:
            pd.DataFrame: Pandas DataFrame read from DB
        """
        df = pd.read_sql_table(table_name, self.engine)
        return df

    def write(self, table_name: str, data: pd.DataFrame):
        """Function writing data to SQL DB

        Args:
            table_name (str): _description_
            data (pd.DataFrame): _description_
        """
        data.to_sql(table_name, self.engine, if_exists='replace', index=False)
