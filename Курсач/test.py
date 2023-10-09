import psycopg2
import argparse


CONFIG = {
            "database": "ambulance",
            "user": "postgres",
            "password": "postgres",
            "host": "192.168.1.105",
            "port": 5432
        }

# conn = psycopg2.connect(**CONFIG)
# cursor = conn.cursor()

# cursor.execute("call GetSickPeopleBySocialStatus('пенсионер')")
# print(cursor.fetchall())

_dict = {
            "main": [],
            "child": []
        }

_dict["main"].append(14)
_dict["child"].append(14)

print(_dict)
