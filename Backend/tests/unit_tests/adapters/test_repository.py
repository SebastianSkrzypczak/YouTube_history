from pandas import DataFrame, testing
from sqlalchemy import create_engine, MetaData, Table, Integer, Column, select, text
from adapters.repository import SqlRepostory
import pytest


def database_setup():
    engine = create_engine("sqlite:///:memory:")
    metadata = MetaData()

    test_table = Table(
        "test_table", metadata, Column("col1", Integer), Column("col2", Integer)
    )
    metadata.create_all(engine)

    with engine.connect() as connection:
        connection.execute(test_table.insert().values(col1=1, col2=3))
        connection.execute(test_table.insert().values(col1=2, col2=4))
        connection.commit()

    return engine


def test_read_db_successful():
    mock_data = DataFrame({"col1": [1, 2], "col2": [3, 4]})
    engine = database_setup()
    sql_repo = SqlRepostory(engine=engine)
    result = sql_repo.read(table_name="test_table")
    result = DataFrame(result)

    testing.assert_frame_equal(mock_data, result)


def test_read_db_error_wrong_table_name():
    engine = database_setup()
    sql_repo = SqlRepostory(engine=engine)
    table_name = "wrong_table_name"
    with pytest.raises(ValueError):
        sql_repo.read(table_name=table_name)


def test_write_successful():
    engine = create_engine("sqlite:///:memory:")
    table_name = "test_table"
    data = DataFrame({"col1": [1, 2], "col2": [3, 4]})
    sql_repo = SqlRepostory(engine=engine)
    sql_repo.write(table_name=table_name, data=data)
    with engine.connect() as connection:
        rows = connection.execute(text("SELECT * FROM test_table"))
    result = DataFrame(rows)

    testing.assert_frame_equal(result, data)
