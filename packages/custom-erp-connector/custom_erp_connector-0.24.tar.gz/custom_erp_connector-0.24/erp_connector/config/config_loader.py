import json
import os

from erp_connector.utils.singleton import SingletonMeta
from erp_connector.utils.custlogging import LoggerProvider
from erp_connector.service.event_service import publish_event, get_request_data
from erp_connector.utils.custlogging import CustomLogHandler

logger = LoggerProvider().get_logger(os.path.basename(__file__))

logs = []
log_handler = CustomLogHandler(logs)
logger.addHandler(log_handler)


class CustomErpConnectorConfig(metaclass=SingletonMeta):
    def __init__(self, config_dict):
        self._config = config_dict

    @property
    def dbType(self):
        return self._config.get("dbType")

    @property
    def connectionDetails(self):
        return self._config.get("connectionDetails")

    @property
    def env(self):
        return self._config.get("env")

    @property
    def authToken(self):
        return self._config.get("authToken")

    @property
    def erpInstanceId(self):
        return self._config.get("erpInstanceId")


class ConfigLoader(metaclass=SingletonMeta):

    def __init__(self, config_path,trace_id):
        self.config_path = config_path
        self.trace_id = trace_id

    def load(self):
        with open(self.config_path, 'r') as file:
            config_dict = json.load(file)
            logger.info("config loaded")
            publish_event(get_request_data(self.trace_id, "", "", ""),logs)
        return CustomErpConnectorConfig(config_dict)
