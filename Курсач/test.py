import psycopg2
import argparse
from inspect import getmembers, isfunction
from typing import Dict, Callable

import complex_requests, requests

CONFIG = {
            "database": "ambulance",
            "user": "postgres",
            "password": "postgres",
            "host": "192.168.0.107",
            "port": 5432
        }

conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()

COLUMNS_NAMES = {'sick_people_id': 'Идентификатор больного', 
                 'full_name': 'ФИО', 
                 'birth_date': 'Дата рождения',
                 'social_status_id': 'Идентификатор социального статуса',
                 'phone_number': 'Номер телефона', 
                 'address': 'Адрес',
                 'call_request_id': 'Идентифиатор заявки на вызов', 
                 'call_date_time': 'Дата заявки на вызов', 
                 'call_reason_id': 'Идентификатор причины вызова', 
                 'money_payment': 'Оплата', 
                 'call_reason_name': 'Причина вызова', 
                 'first_aid_station_id': 'Идентификатор скорой помощи', 
                 'first_aid_station_number': 'Номер скорой помощи', 
                 'city_district': 'Район города',
                 'employees_amount': 'Количество сотрудников',
                 'phone_number': 'Номер телефона',
                 'address': 'Адрес',
                 'procedure_id': 'Идентификатор процедуры',
                 'procedure_name': 'Наименование процедуры', 
                 'procedure_application_id': 'Идентификатор процедуры и заявки на вызов', 
                 'application_id': 'Идентификатор заявки на вызов',
                 'social_status_name': 'Социальный статус', 
                 'abanoned_station_id': 'Идентификатор заброшенной станции скорой помощи', 
                 'station_number': 'Номер станции скорой помощи',
                 'healthy_people_id': 'Идентификатор здорового',
                 'new_sick_person_id': 'Идентификатор больного',
                 'new_full_name': 'ФИО', 
                 'new_birth_date': 'Дата рождения',
                 'new_phone_number': 'Номер телефона', 
                 'new_address': 'Адрес'
                 }

REVERSED_COLUMNS_NAMES = {value: key for key, value in COLUMNS_NAMES.items()}

print(REVERSED_COLUMNS_NAMES)
# columns_names = []
# for table_name in TABLES_DICT.values():
#     cursor.execute("SELECT * FROM {} LIMIT 0".format(table_name))

#     for desc in cursor.description: columns_names.append(desc[0])

# print(columns_names)
