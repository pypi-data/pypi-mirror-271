import json
import os

from erp_connector.db.mssql_connector import MsSqlConnector
from erp_connector.db.mysql_connector import MySqlConnector
from erp_connector.db.oracle_connector import OracleConnector
from erp_connector.db.postgresql_connector import PostgresSQLConnector
from erp_connector.utils.custlogging import LoggerProvider
from erp_connector.service.event_service import publish_event, get_request_data
from erp_connector.utils.custlogging import CustomLogHandler

logger = LoggerProvider().get_logger(os.path.basename(__file__))

logs = []
log_handler = CustomLogHandler(logs)
logger.addHandler(log_handler)


class ConfigLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, 'r') as file:
            config = json.load(file)
        return config


class ConnectionLoader:
    @staticmethod
    def load_connector(custom_erp_connector_config,trace_id):
        connector = ConnectorFactory.create_connector(custom_erp_connector_config,trace_id)
        logger.info("db config loaded")
        publish_event(get_request_data(trace_id, "", "", ""),logs)
        return connector


class ConnectorFactory:
    @staticmethod
    def create_connector(erp_connector_config,trace_id):
        logger.info("loading db config")
        db_type = erp_connector_config.dbType
        connection_details = erp_connector_config.connectionDetails
        if db_type == 'mysql':
            logger.info("creating mysql connector")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return MySqlConnector(connection_details)
        elif db_type == 'postgresql':
            logger.info("creating postgresql connector")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return PostgresSQLConnector(connection_details)
        elif db_type == 'mssql':
            logger.info("creating mssql connector")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return MsSqlConnector(connection_details)
        elif db_type == 'oracle':
            logger.info("creating oracle connector")
            publish_event(get_request_data(trace_id, "", "", ""), logs)
            return OracleConnector(connection_details)
        else:
            raise ValueError("Invalid db connector config: dbName must be 'mysql' or 'postgresql'")
