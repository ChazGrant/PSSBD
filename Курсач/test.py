import psycopg2
import argparse
from inspect import getmembers, isfunction
from typing import Dict, Callable

import complex_requests, requests

CONFIG = {
            "database": "ambulance",
            "user": "ambulance_operator",
            "password": "(fN6Pn!5",
            "host": "127.0.0.1",
            "port": 5432
        }


# ambulance_operator (fN6Pn!5
# doctor u8YVX,:2
# nurse ]Lg4SSr4

conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()
