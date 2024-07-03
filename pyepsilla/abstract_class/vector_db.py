from abc import ABC, abstractmethod
from typing import Optional, Union


class AbstractVectordb(ABC):
    @abstractmethod
    def __init__(self, project_id: str, db_id: str, api_key: str, public_endpoint: str, headers: dict = None):
        pass

    @abstractmethod
    def list_tables(self):
        pass

    @abstractmethod
    def create_table(self, table_name: str, table_fields: list[dict] = None, indices: list[dict] = None):
        pass

    @abstractmethod
    def drop_table(self, table_name: str):
        pass

    @abstractmethod
    def insert(self, table_name: str, records: list[dict]):
        pass

    @abstractmethod
    def upsert(self, table_name: str, records: list[dict]):
        pass

    @abstractmethod
    def query(self, table_name: str, query_text: str = None, query_index: str = None, query_field: str = None, query_vector: Union[list, dict] = None, response_fields: Optional[list] = None, limit: int = 2, filter: Optional[str] = None, with_distance: Optional[bool] = False, facets: Optional[list[dict]] = None):
        pass

    @abstractmethod
    def delete(self, table_name: str, primary_keys: Optional[list[Union[str, int]]] = None, ids: Optional[list[Union[str, int]]] = None, filter: Optional[str] = None):
        pass
