import sqlite3
import os
import uuid
from datetime import datetime, timedelta
from erp_connector.clients.euclid_client import EuclidClient
from erp_connector.utils.custlogging import LoggerProvider

logger = LoggerProvider().get_logger(os.path.basename(__file__))


def create_table():
    conn = sqlite3.connect('scheduler_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scheduler_data
                 (id INTEGER PRIMARY KEY,
                 created_at TEXT,
                 trace_id TEXT,
                 command TEXT,
                 command_id TEXT,
                 erp_instance_id TEXT,
                 log_level TEXT,
                 log_message TEXT)''')
    conn.commit()
    conn.close()


def insert_data():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('scheduler_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO scheduler_data (started_at,updated_at) VALUES (?, ?)",
              (start_time, start_time))
    conn.commit()
    row_id = c.lastrowid
    conn.close()
    return row_id


def update_data(row_id, command, command_id, status):
    conn = sqlite3.connect('scheduler_data.db')
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c = conn.cursor()
    c.execute("UPDATE scheduler_data SET updated_at = ?, command = ?, command_id = ?, status = ? WHERE id = ?",
              (updated_at, command, command_id, status, row_id))
    conn.commit()
    c.execute("SELECT * FROM scheduler_data WHERE id = ?", (row_id,))
    updated_row = c.fetchone()

    conn.close()
    return updated_row


def add_event(event):
    conn = sqlite3.connect('scheduler_data.db')
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c = conn.cursor()
    c.execute(
        "INSERT INTO scheduler_data (created_at,trace_id,log_level,log_message,erp_instance_id,command,command_id) VALUES (?, ?,?,?,?,?,?)",
        (updated_at, event['trace_id'], event['log_level'], event['log_message'], event['erp_instance_id'],
         event['command'], event['command_id']))
    conn.commit()
    row_id = c.lastrowid
    c.execute("SELECT * FROM scheduler_data WHERE id = ?", (row_id,))
    updated_row = c.fetchone()

    conn.close()
    return updated_row


def delete_old_records():
    conn = sqlite3.connect('scheduler_data.db')
    c = conn.cursor()
    one_month_ago = datetime.now() - timedelta(days=30)
    c.execute("DELETE FROM scheduler_data WHERE start_time < ?", (one_month_ago,))
    conn.commit()
    conn.close()


def publish_event(request_data, logs):
    log = logs[0]
    event = {
        "_id": str(uuid.uuid4()),
        "trace_id": request_data.get("traceId",""),
        "command_id": request_data.get("commandId",""),
        "command": request_data.get("command",""),
        "erp_instance_id": request_data.get("erpInstanceId",""),
        "log_level": log.get("level",""),
        "log_message": log.get("message","")
    }
    logs.clear()
    event_row = add_event(event)
    datetime_object = datetime.strptime(event_row[1], '%Y-%m-%d %H:%M:%S')
    iso_format = datetime_object.isoformat()
    event['created_at'] = iso_format
    euclid_client = EuclidClient()
    euclid_client.post_events(event)


def get_request_data(trace_id, command_id, command, erp_instance_id):
    if command_id is None:
        command_id = ""
    return {'traceId': trace_id, 'commandId': command_id, 'command': command, 'erpInstanceId': erp_instance_id}
