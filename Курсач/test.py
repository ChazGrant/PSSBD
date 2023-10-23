import psycopg2
import argparse
from inspect import getmembers, isfunction
from typing import Dict, Callable

import complex_requests, requests

CONFIG = {
            "database": "ambulance",
            "user": "postgres",
            "password": "postgres",
            "host": "192.168.0.106",
            "port": 5432
        }

conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()

# ambulance_operator (fN6Pn!5
# doctor u8YVX,:2
# nurse ]Lg4SSr4

QUERIES = ['leftOuterJoinRequest', 'requestOnRequestLeftJoin', 'rightOuterJoinRequest', 
'symmetricInnerRequestWithConditionDateOne', 'symmetricInnerRequestWithConditionDateTwo', 
'symmetricInnerRequestWithConditionExternalKeyOne', 'symmetricInnerRequestWithConditionExternalKeyTwo', 
'symmetricInnerRequestWithoutConditionOne', 'symmetricInnerRequestWithoutConditionThree', 
'symmetricInnerRequestWithoutConditionTwo', 'queryOnTotalQuery', 'totalQueryWithDataCondition', 
'totalQueryWithDataGroupCondition', 'totalQueryWithGroupCondition',  'totalQueryWithSubquery', 
'totalQueryWithoutCondition']

for query in QUERIES:
    query = query.lower()
    cursor.execute("select pg_get_functiondef(oid) from pg_proc where proname = '{}';".format(query))

    print(query)
    try:
        # cursor.fetchone()[0].replace("function", "")
        print(cursor.fetchone()[0].replace("function", ""))
    except TypeError:
        cursor.execute("SELECT pg_get_viewdef('{}', true);".format(query))
        print(cursor.fetchone()[0])
    print()
