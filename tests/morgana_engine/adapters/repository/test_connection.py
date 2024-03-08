import pytest
from pathlib import Path
from morgana_engine.models.schema import Schema
from morgana_engine.adapters.repository.connection import (
    Connection,
    FSConnection,
)
from morgana_engine.utils.uri import path_to_uri


class TestConnection:
    def test_uri(self):
        conn = Connection()
        with pytest.raises(NotImplementedError):
            conn.uri

    def test_storage_options(self):
        conn = Connection()
        with pytest.raises(NotImplementedError):
            conn.storage_options

    def test_schema(self):
        conn = Connection()
        with pytest.raises(NotImplementedError):
            conn.schema

    def test_list_files(self):
        conn = Connection()
        with pytest.raises(NotImplementedError):
            conn.list_files()

    def test_list_partition_files(self):
        conn = Connection()
        with pytest.raises(NotImplementedError):
            conn.list_partition_files("column_name")

    def test_access(self):
        conn = Connection()
        with pytest.raises(NotImplementedError):
            conn.access("table_name")


class TestFSConnection:
    def test_list_files_database_schema(self):
        conn = FSConnection("tests/data")
        with pytest.raises(ValueError):
            conn.list_files()

    def test_list_partition_files_database_schema(self):
        conn = FSConnection("tests/data")
        with pytest.raises(ValueError):
            conn.list_partition_files("column1")

    def test_access(self):
        conn = FSConnection("tests/data")
        with pytest.raises(ValueError):
            conn.access("non_existent_table")
        sub_conn = conn.access("usinas")
        assert isinstance(sub_conn, FSConnection)
        assert sub_conn.uri == path_to_uri(
            str(Path("tests/data/usinas").resolve()), "file"
        )
        assert sub_conn.schema == Schema(
            {
                "uri": "./data/usinas/schema.json",
                "name": "usinas",
                "description": "",
                "fileType": ".parquet.gzip",
                "columns": [
                    {"name": "id", "type": "int"},
                    {"name": "codigo", "type": "string"},
                    {"name": "nome", "type": "string"},
                    {"name": "capacidade_instalada", "type": "float"},
                    {"name": "latitude", "type": "float"},
                    {"name": "longitude", "type": "float"},
                    {"name": "data_inicio_operacao", "type": "date"},
                    {"name": "data_inicio_simulacao", "type": "date"},
                    {"name": "subsistema_geografico", "type": "string"},
                    {"name": "subsistema_eletrico", "type": "string"},
                ],
                "partitions": [],
            }
        )

    def test_list_files_table_schema(self):
        conn = FSConnection("tests/data/usinas")
        conn.list_files()

    def test_list_partition_files_table_schema(self):
        conn = FSConnection("tests/data/usinas")
        files = conn.list_partition_files("codigo")
        assert len(files) == 0
        conn = FSConnection("tests/data/usinas_part_subsis")
        files = conn.list_partition_files("subsistema_geografico")
        assert len(files) == 2
