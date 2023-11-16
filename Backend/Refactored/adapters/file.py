from abc import ABC, abstractmethod
import logging
import json


class AbstractFile(ABC):

    @abstractmethod
    def read():
        pass


class JSONFIle:
    '''Class to handle JSON files'''

    def __init__(self, file_path: str) -> None:
        self.file = file_path

    def read(self) -> json:
        with open(self.file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        json_lines = ''.join(lines)
        try:
            json_data = json.loads(json_lines)
        except json.JSONDecodeError as e:
            logging.debug(e)
        return json_data
