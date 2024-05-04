# custom-erp-connector

Custom ERP Connector is a Python package designed to streamline integration with various ERP systems. It offers functionalities to connect to their respective databases via configuration, fetch data, and process it, allowing users to build custom connectors tailored to their specific requirements.

# Package Generation

To generate the package locally, run the following command:

``python3.11 setup.py sdist``

# Installation

Once the package is generated, it will be in the form of a tar.gz file, such as custom_erp_connector-0.2.tar.gz. Install it using the following command:

```pip install custom_erp_connector-0.2.tar.gz```

# Usage

You can trigger the installed package as follows:

```python3.11 -m erp_connector.scheduler db-config.json```

# sample db-config.json file

This file contains the configuration details required to connect to the database, such as the database type, host, credentials, environment, authentication token, and ERP instance ID.
Feel free to modify the db-config.json file according to your specific setup and requirements.

```
{
  "dbType": "mysql",
  "connectionDetails": {
    "host": "localhost",
    "database": "",
    "user": "",
    "password": ""
  },
  "env": "sandbox",
  "authToken": "",
  "erpInstanceId": ""
}

