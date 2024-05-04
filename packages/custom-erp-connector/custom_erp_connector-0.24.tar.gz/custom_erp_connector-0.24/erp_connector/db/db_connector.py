from abc import ABC, abstractmethod


class DBConnector(ABC):
    def __init__(self, connection_details):
        self.connection_details = connection_details
        self.connection = None

    @abstractmethod
    def connect_db(self):
        pass

    @abstractmethod
    def fetch_data(self, query):
        pass

    @abstractmethod
    def generate_query(self, json_data):
        pass

    @abstractmethod
    def get_total_table_count(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass
