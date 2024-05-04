import json
import os
from datetime import date
from decimal import Decimal

import pyodbc
from erp_connector.db.db_connector import DBConnector
from erp_connector.utils.mysql_query_utils import generate_data_query
from erp_connector.utils.custlogging import LoggerProvider, CustomLogHandler
from erp_connector.service.event_service import publish_event, get_request_data

logger = LoggerProvider().get_logger(os.path.basename(__file__))

logs = []
log_handler = CustomLogHandler(logs)
logger.addHandler(log_handler)


class MsSqlConnector(DBConnector):

    def __init__(self, connection_details):
        super().__init__(connection_details)
        self.connection = None

    def connect_db(self, trace_id):
        try:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.connection_details['host']},{self.connection_details['port']};"
                f"DATABASE={self.connection_details['database']};"
                f"UID={self.connection_details['user']};"
                f"PWD={self.connection_details['password']}"
            )
            self.connection = pyodbc.connect(conn_str)
            logger.info(f"Connected to MSSQL Server database: {self.connection_details['database']}")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return self
        except pyodbc.Error as e:
            logger.error(f"Error connecting to MSSQL Server database: {e}")

    def fetch_data(self, query, trace_id):
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
        except pyodbc.Error as e:
            logger.error(f"Error fetching data from MSSQL Server database: {e}")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return None

    def generate_query(self, json_data):
        return generate_data_query(json_data)

    def get_total_table_count(self, trace_id):
        """
        Get the total count of tables present in the connected SQL Server database.
        :return: Total count of tables in the database
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM sys.tables")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except pyodbc.Error as e:
            logger.error(f"Error getting table count from SQL Server database: {e}")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return None

    def close_connection(self,trace_id):
        if self.connection:
            self.connection.close()
            logger.info("Connection to MSSQL database closed")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
