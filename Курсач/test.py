import psycopg2
import argparse
from inspect import getmembers, isfunction
from typing import Dict, Callable

import complex_requests, requests

CONFIG = {
            "database": "ambulance",
            "user": "postgres",
            "password": "postgres",
            "host": "127.0.0.1",
            "port": 5432
        }

conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()
from CONSTANTS import QUERIES, PARAMS


def getValue(type: str):
    if type == "birth_date" or type == "call_date_time":
        return "'1999-01-01'"
    else:
        return "'4'"

columns_names = []
for idx, query in enumerate(QUERIES.values()):
    params_mask = PARAMS[idx].split(" ")
    print(idx)
    print(params_mask)
    if not params_mask == ['']:
        cursor.execute("SELECT * FROM {}({}) LIMIT 0".format(query, ", ".join\
                                                             ([getValue(param_mask) for param_mask in params_mask])))
    else:
        cursor.execute("SELECT * FROM {} LIMIT 0".format(query))

    for desc in cursor.description: columns_names.append(desc[0])

print(columns_names)
