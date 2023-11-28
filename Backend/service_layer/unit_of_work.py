"""This module defines the `AbstractUnitOfWork` and `SqLiteUnitOfWork` classes."""


from abc import ABC, abstractmethod
from sqlalchemy import create_engine, inspect
from adapters import repository


class AbstractUnitOfWork(ABC):
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError


class SqLiteUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        super().__init__()
        self.engine = create_engine("sqlite:///history.db")
        self.inspector = inspect(self.engine)
        self.videos = None
        self.damaged_urls = None

    def __enter__(self):
        if self.inspector.has_table("videos"):
            self.videos = repository.SqlRepostory(self.engine).read("videos")
        if self.inspector.has_table("damaged_urls"):
            self.damaged_urls = repository.SqlRepostory(self.engine).read(
                "damaged_urls"
            )

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def commit(self, table_name, data):
        repository.SqlRepostory(self.engine).write(table_name, data)

    def rollback(self):
        pass
