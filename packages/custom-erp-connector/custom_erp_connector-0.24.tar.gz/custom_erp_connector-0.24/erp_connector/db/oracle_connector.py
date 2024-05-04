import json
import os
import traceback
from datetime import date
from decimal import Decimal

import oracledb
from erp_connector.db.db_connector import DBConnector
from erp_connector.utils.mysql_query_utils import generate_data_query
from erp_connector.utils.custlogging import LoggerProvider
from erp_connector.utils.custlogging import CustomLogHandler
from erp_connector.service.event_service import publish_event, get_request_data

logger = LoggerProvider().get_logger(os.path.basename(__file__))

logs = []
log_handler = CustomLogHandler(logs)
logger.addHandler(log_handler)


class OracleConnector(DBConnector):

    def __init__(self, connection_details):
        super().__init__(connection_details)
        self.connection = None

    def connect_db(self,trace_id):
        try:
            dsn = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={self.connection_details['host']})(PORT={self.connection_details['port']}))(CONNECT_DATA=(SERVICE_NAME={self.connection_details['database']})))"
            self.connection = oracledb.connect(user=self.connection_details['user'], password=self.connection_details['password'],
                              dsn=dsn)
            logger.info(f"Connected to Oracle database: {self.connection_details['database']}")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return self
        except Exception as e:
            logger.error(f"Error connecting to Oracle database: {e}")

    def fetch_data(self, query,trace_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            # Fetch all rows as a list of tuples
            rows = cursor.fetchall()

            # Convert Decimal objects to float
            data = []
            for row in rows:
                converted_row = {}
                for idx, value in enumerate(row):
                    column_name = cursor.description[idx][0]
                    if isinstance(value, Decimal):
                        converted_row[column_name] = float(value)
                    elif isinstance(value, date):
                        converted_row[column_name] = value.strftime('%Y-%m-%d')
                    else:
                        converted_row[idx] = value
            data.append(dict(zip([desc[0] for desc in cursor.description], converted_row)))

            cursor.close()
            return data
        except Exception as e:
            logger.error(f"Error fetching data from Oracle database: {e}")
            traceback.print_exc()
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return None

    def generate_query(self, json_data):
        return generate_data_query(json_data)

    def get_total_table_count(self,trace_id):
        """
        Get the total count of tables present in the connected Oracle database.
        :return: Total count of tables in the database
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM all_tables")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except Exception as e:
            logger.error(f"Error getting table count from Oracle database: {e}")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return None

    def close_connection(self,trace_id):
        if self.connection:
            self.connection.close()
            logger.info("Connection to Oracle database closed")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
