import json
import os
import traceback

from rich.progress import Progress
import time
import sys
import uuid

from erp_connector.clients.one_integration_client import OneIntegrationClient
from erp_connector.utils.file_utils import zip_folder
from erp_connector.config.config_loader import ConfigLoader
from erp_connector.db.db_loader import ConnectionLoader
from erp_connector.utils.custlogging import LoggerProvider
from erp_connector.service.event_service import publish_event, get_request_data
from erp_connector.utils.custlogging import CustomLogHandler

logger = LoggerProvider().get_logger(os.path.basename(__file__))

logs = []
log_handler = CustomLogHandler(logs)
logger.addHandler(log_handler)


def process_connector(db_connector, one_integration_client, erp_instance_id):
    trace_id = str(uuid.uuid4())
    command = ""
    command_id = ""
    logger.info("running process connector ")
    publish_event(get_request_data(trace_id, command_id, command, erp_instance_id), logs)
    try:
        get_command_response = one_integration_client.get_command()
        get_command_result = get_command_response['result']
        command = get_command_result['command']
        command_id = get_command_result.get('commandId', "")
        logger.info(f"received command: {command}")
        publish_event(get_request_data(trace_id, command_id, command, erp_instance_id), logs)
        if command == 'DATA_EXTRACTION':
            json_data = get_command_result['metadata']['erpConfig']['tables']
            query_metadata_list = db_connector.generate_query(json_data)
            current_path = os.getcwd()
            output_folder_path = os.path.join(current_path, 'output')
            zip_folder_path = os.path.join(current_path, 'output_zip')
            logger.info(f"query_metadata: {query_metadata_list}")
            for query_metadata in query_metadata_list:
                table_name = query_metadata["tableName"]
                select_query = query_metadata["query"]
                json_data = db_connector.fetch_data(select_query, trace_id)
                if json_data is None:
                    raise RuntimeError("Error executing database query")
                local_file_path = f"{output_folder_path}/{table_name}.json"
                os.makedirs(output_folder_path, exist_ok=True)
                os.makedirs(zip_folder_path, exist_ok=True)
                with open(local_file_path, 'w') as json_file:
                    json.dump(json_data, json_file, indent=4)

            zip_file_path = zip_folder(output_folder_path, zip_folder_path, "data.zip")
            publish_event(get_request_data(trace_id, command_id, command, erp_instance_id), logs)
            presigned_response = one_integration_client.get_presign("data.zip", command_id, trace_id)
            presigned_url = presigned_response['result']['payload']
            one_integration_client.upload_to_s3(presigned_url, zip_file_path, trace_id)
            post_response = one_integration_client.post_command(presigned_url, command_id, trace_id)
            logger.info(f"{post_response['message']}")
            publish_event(get_request_data(trace_id, command_id, command, erp_instance_id), logs)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        traceback.print_exc()
        publish_event(get_request_data(trace_id, command_id, command, erp_instance_id), logs)


def verifying_config(config_path):
    trace_id = str(uuid.uuid4())
    progress = Progress()
    task_load_config = progress.add_task("[cyan]Verifying config...", total=8)
    with progress:
        time.sleep(1)
        progress.update(task_load_config, advance=1)
        config_loader = ConfigLoader(config_path, trace_id)
        time.sleep(1)
        progress.update(task_load_config, advance=1)
        custom_erp_connector_config = config_loader.load()
        time.sleep(1)
        progress.update(task_load_config, advance=1)
        one_integration_client = OneIntegrationClient(custom_erp_connector_config)
        time.sleep(1)
        progress.update(task_load_config, advance=1)
        try:
            ping_response = one_integration_client.ping()
            if ping_response["status"] == 200:
                logger.info(f"connection established")
                publish_event(get_request_data(trace_id, "", "", custom_erp_connector_config.erpInstanceId), logs)
            else:
                logger.error("connection failure. please check your api connection details")
                publish_event(get_request_data(trace_id, "", "", custom_erp_connector_config.erpInstanceId), logs)
                sys.exit(1)
        except Exception as e:
            error_message = "Connection failure: Unable to connect with Clear. Please verify the configuration details or contact Clear support."
            logger.error(error_message)
            publish_event(get_request_data(trace_id, "", "", custom_erp_connector_config.erpInstanceId), logs)
            sys.exit(1)

        time.sleep(1)
        progress.update(task_load_config, advance=1)
        db_connector = ConnectionLoader.load_connector(custom_erp_connector_config, trace_id)
        time.sleep(1)
        progress.update(task_load_config, advance=1)
        db_connector = db_connector.connect_db(trace_id)
        time.sleep(1)
        progress.update(task_load_config, advance=1)
        if db_connector is None:
            logger.error(f"please check your specified config there is some issue with it")
            publish_event(get_request_data(trace_id, "", "", custom_erp_connector_config.erpInstanceId), logs)
            sys.exit(1)
        total_table_count = db_connector.get_total_table_count(trace_id)
        if total_table_count is None:
            logger.error("failed to connect db. please check your db configuration")
            publish_event(get_request_data(trace_id, "", "", custom_erp_connector_config.erpInstanceId), logs)
            sys.exit(1)
        else:
            logger.info(f"connected to db and having total tables : {total_table_count}")
            publish_event(get_request_data(trace_id, "", "", custom_erp_connector_config.erpInstanceId), logs)
        time.sleep(1)
        progress.update(task_load_config, advance=1)
        logger.info("Config verified: API and DB connections established. Scheduled for DATA_EXTRACTION command.")
        publish_event(get_request_data(trace_id, "", "", custom_erp_connector_config.erpInstanceId), logs)
        return {
            "client": one_integration_client,
            "dbConnector": db_connector,
            "erpInstanceId": custom_erp_connector_config.erpInstanceId
        }
