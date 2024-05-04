import os

import psycopg2
from erp_connector.db.db_connector import DBConnector
from erp_connector.utils.custlogging import LoggerProvider, CustomLogHandler
from erp_connector.service.event_service import publish_event, get_request_data

logger = LoggerProvider().get_logger(os.path.basename(__file__))

logs = []
log_handler = CustomLogHandler(logs)
logger.addHandler(log_handler)


class PostgresSQLConnector(DBConnector):

    def __init__(self, connection_details):
        super().__init__(connection_details)
        self.connection = None

    def connect_db(self, trace_id):
        try:
            self.connection = psycopg2.connect(
                host=self.connection_details['host'],
                user=self.connection_details['user'],
                password=self.connection_details['password'],
                database=self.connection_details['database']
            )
            logger.info(f"Connected to PostgreSQL database: {self.connection_details['database']}")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return self
        except psycopg2.Error as e:
            logger.error(f"Error connecting to PostgreSQL database: {e}")

    def fetch_data(self, query, trace_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return data
        except psycopg2.Error as e:
            logger.error(f"Error fetching data from PostgreSQL database: {e}")
            publish_event(get_request_data(trace_id, "", "", ""), logs)

    def get_total_table_count(self,trace_id):
        """
        Get the total count of tables present in the connected PostgreSQL database.
        :return: Total count of tables in the database
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except psycopg2.Error as e:
            logger.error(f"Error getting table count from PostgreSQL database: {e}")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return None

    def close_connection(self,trace_id):
        if self.connection:
            self.connection.close()
            logger.info("Connection to PostgreSQL database closed")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
