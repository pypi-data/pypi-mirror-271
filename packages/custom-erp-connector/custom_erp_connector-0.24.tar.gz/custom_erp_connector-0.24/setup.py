#!/usr/bin/env python
from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

package_name = "custom_erp_connector"

package_version = "0.24"
description = """custom-erp-connector"""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Dinesh Sharma",
    author_email="dinesh.sharma@clear.in",
    url="https://github.com/ClearTax/custom-erp-connector",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'run_scheduler = scheduler:run_scheduler'
        ]
    },
    install_requires=[
        "mysql-connector-python==8.3.0",
        "psycopg2==2.9.9",
        "requests==2.31.0",
        "APScheduler==3.10.4",
        "pyodbc==5.1.0",
        "sqlparse==0.4.3",
        "SQLAlchemy==1.4.46",
        "python-dateutil==2.8.2",
        "h2==4.1.0",
        "simplejson==3.18.3",
        "sqlglot==18.7.0",
        "oracledb==2.1.2"
    ]
)
