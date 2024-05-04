import argparse
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from erp_connector.service.connector_service import process_connector, verifying_config
import time
from erp_connector.service.event_service import create_table


def run_scheduler(config_path):
    trace_id = str(uuid.uuid4())
    create_table()
    config_response = verifying_config(config_path)
    erp_instance_id = config_response["erpInstanceId"]
    db_connector = config_response["dbConnector"]
    one_integration_client = config_response["client"]
    scheduler = BackgroundScheduler(daemon=True)
    process_connector(db_connector,one_integration_client,erp_instance_id)
    scheduler.add_job(process_connector, 'interval', minutes=1, max_instances=1, args=(db_connector,one_integration_client,erp_instance_id))
    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        db_connector.close_connection(trace_id)
        scheduler.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ERP Connector Scheduler')
    parser.add_argument('config_path', type=str, help='Path to configuration file')
    args = parser.parse_args()
    run_scheduler(args.config_path)
