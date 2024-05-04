import json
import os
from datetime import date
from decimal import Decimal

import mysql.connector
from erp_connector.db.db_connector import DBConnector
from erp_connector.utils.mysql_query_utils import generate_data_query
from erp_connector.utils.custlogging import LoggerProvider
from erp_connector.service.event_service import publish_event, get_request_data
from erp_connector.utils.custlogging import CustomLogHandler

logger = LoggerProvider().get_logger(os.path.basename(__file__))

logs = []
log_handler = CustomLogHandler(logs)
logger.addHandler(log_handler)


class MySqlConnector(DBConnector):

    def __init__(self, connection_details):
        super().__init__(connection_details)
        self.connection = None

    def connect_db(self,trace_id):
        try:
            self.connection = mysql.connector.connect(
                host=self.connection_details['host'],
                user=self.connection_details['user'],
                password=self.connection_details['password'],
                database=self.connection_details['database']
            )
            logger.info(f"Connected to MySQL database: {self.connection_details['database']}")
            publish_event(get_request_data(trace_id, "", "", ""),logs)
            return self
        except mysql.connector.Error as e:
            logger.error(f"Error connecting to MySQL database: {e}")
            publish_event(get_request_data(trace_id, "", "", ""),logs)
            return None

    def fetch_data(self, query,trace_id):
        try:
            cursor = self.connection.cursor(dictionary=True)  # Use dictionary cursor to fetch rows as dictionaries
            cursor.execute(query)
            data = cursor.fetchall()

            # Convert Decimal objects to float
            for row in data:
                for key, value in row.items():
                    if isinstance(value, Decimal):
                        row[key] = float(value)
                    elif isinstance(value, date):
                        row[key] = value.strftime('%Y-%m-%d')

            cursor.close()
            return json.dumps(data)  # Convert data to JSON string
        except mysql.connector.Error as e:
            logger.error(f"Error fetching data from MySQL database: {e}")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return None  # Return None if there's an error

    def generate_query(self, json_data):
        return generate_data_query(json_data)

    def get_total_table_count(self,trace_id):
        """
        Get the total count of tables present in the connected MySQL database.
        :return: Total count of tables in the database
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s",
                           (self.connection_details['database'],))
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except mysql.connector.Error as e:
            logger.error(f"Error getting table count from MySQL database: {e}")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return None

    def close_connection(self,trace_id):
        if self.connection:
            self.connection.close()
            logger.info("Connection to MySQL database closed")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
