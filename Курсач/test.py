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


# ambulance_operator (fN6Pn!5
# doctor u8YVX,:2
# nurse ]Lg4SSr4

conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()
username = "ambulance_operator"
query = "SELECT table_name, privilege_type FROM \
    information_schema.table_privileges WHERE grantee = '{}' \
        AND table_catalog = 'ambulance' \
            AND table_schema = 'public';".format(username)

user_rights = dict()
cursor.execute(query)
user_rights[username] = dict()
for data in cursor.fetchall():
    if data[0] not in user_rights[username]:
        user_rights[username][data[0]] = [data[1]]
    else:
        user_rights[username][data[0]].append(data[1])

print(user_rights)
# cursor.execute("call GetSickPeopleBySocialStatus('пенсионер')")
# print(cursor.fetchall())

