import json
import pytest
from unittest.mock import mock_open, patch
from adapters.file import JSONFIle


def test_read_successful():
    file_path = "test.json"
    mock_json_data = {"key": "value"}

    with patch("builtins.open", mock_open(read_data=json.dumps(mock_json_data))):
        json_file = JSONFIle(file_path)
        result = json_file.read()

        assert result == mock_json_data


def test_FileNotFound_error():
    file_path = "test.json"

    with pytest.raises(FileNotFoundError):
        json_file = JSONFIle(file_path)
        json_file.read()


def test_invalid_data_in_file():
    file_path = "test.json"
    invalid_json_data = "invalid_data"

    with patch("builtins.open", mock_open(read_data=invalid_json_data)):
        json_file = JSONFIle(file_path)

        with pytest.raises(json.JSONDecodeError):
            json_file.read()
