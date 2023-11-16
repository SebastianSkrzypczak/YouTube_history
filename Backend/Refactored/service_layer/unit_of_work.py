from sqlalchemy import create_engine, inspect
from adapters import repository
from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError


class SqLiteUnitOfWork(AbstractUnitOfWork):

    def __init__(self) -> None:
        super().__init__()
        self.engine = create_engine('sqlite:///history.db')
        self.inspector = inspect(self.engine)
        self.videos = None

    def __enter__(self):
        if self.inspector.has_table('videos'):
            self.videos = repository.SqlRepostory(self.engine).read('videos')

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def commit(self, data):
        repository.SqlRepostory(self.engine).write('videos', data)

    def rollback(self):
        pass
