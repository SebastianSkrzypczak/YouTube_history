"""This module provides abstract and concrete classes for handling reading data from files.
"""

from abc import ABC, abstractmethod
import logging
import json

logger = logging.getLogger(__name__)


class AbstractFile(ABC):
    @abstractmethod
    def read(self):
        pass


class JSONFIle:
    def __init__(self, file_path: str) -> None:
        self.file = file_path

    def read(self) -> json:
        with open(self.file, "r", encoding="utf-8") as f:
            try:
                lines = f.readlines()
            except FileNotFoundError as e:
                logger.error(e)
                raise
        json_lines = "".join(lines)

        try:
            json_data = json.loads(json_lines)
        except json.JSONDecodeError as e:
            logger.debug(e)
            raise

        return json_data
