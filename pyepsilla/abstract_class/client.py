from abc import ABC, abstractmethod


class AbstractClient(ABC):
    @abstractmethod
    def __init__(self, project_id: str, api_key: str, headers: dict = None):
        pass

    @abstractmethod
    def get_db_list(self):
        pass

    @abstractmethod
    def get_db_info(self, db_id: str):
        pass

    @abstractmethod
    def vectordb(self, db_id: str):
        pass
