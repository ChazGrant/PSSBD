json_example = {
    "call_reason_name": "value",
    "sick_person": {
        "name": "Данил",
        "surname": "Шустов",
        "age": 23,
        "gender": 1,
        "credentials": {
            "passwort_series": "22 34",
            "passport_number": "654 238",
            "additional_info": {
                "country": "ДНР",
                "city": "Донецк",
                "issued by": {
                    "name": "Илья",
                    "surname": "Шатохин",
                    "third_name": "Игоревич"
                }
            }
        }
    },
    "call_date_time": "2023-01-01 12:34:23",
    "money_payment": 1340
}


from CONFIG import CONFIG
import psycopg2
import random
import random_names
import russian_names
from datetime import datetime as dd
import json


def getRandomCallReasonName(cursor) -> str:
    cursor.execute("SELECT COUNT(*) FROM call_reason;")
    call_reason_amount = int(cursor.fetchone()[0])

    random_offset = random.randint(0, call_reason_amount - 1)
    cursor.execute(f"SELECT call_reason_name FROM call_reason OFFSET {random_offset} LIMIT 1;")
    return cursor.fetchone()[0]

def fillJsonDB():
    conn = psycopg2.connect(**CONFIG)
    cursor = conn.cursor()

    for i in range(87500):
        call_reason_name = getRandomCallReasonName(cursor)
        sick_person_name, _, sick_person_surname, sick_person_gender = russian_names.RussianNames().get_person().split(" ")
        sick_person_gender = 1 if sick_person_gender == "True" else 0
        sick_person_age = random.randint(18, 70)
        passport_series = "".join([str(random.randint(0, 9)) for _ in range(4)])
        passport_number ="".join([str(random.randint(0, 9)) for _ in range(6)])
        country = random_names.Country()
        city = random_names.Address().split(",")[2][1:]
        issued_by_name, issued_by_surname, issued_by_third_name, _ = russian_names.RussianNames().get_person().split(" ")
        call_date_time = dd(
            year=random.randint(2017, 2023),
            month=random.randint(1, 12),
            day=random.randint(1, 28),
            hour=random.randint(0, 23),
            minute=random.randint(1, 59),
            second=random.randint(1, 59)
        )
        call_date_time = str(call_date_time)
        money_payment = random.randint(500, 3000)
        json_data = {
            "call_reason_name": call_reason_name,
            "sick_person": {
                "name": sick_person_name,
                "surname": sick_person_surname,
                "age": sick_person_age,
                "gender": sick_person_gender,
                "credentials": {
                    "passport_series": passport_series,
                    "passport_number": passport_number,
                    "additional_info": {
                        "country": country,
                        "city": city,
                        "issued by": {
                            "name": issued_by_name,
                            "surname": issued_by_surname,
                            "third_name": issued_by_third_name,
                        }
                    }
                }
            },
            "call_date_time": call_date_time,
            "money_payment": money_payment
        }

        json_data = json.dumps(json_data)
        cursor.execute("INSERT INTO json_call_requests(call_request_json_data) VALUES(%s)", (json_data, ))

        if (i + 1) % 250 == 0:
            print("%s/87500" % (i + 1))
            conn.commit()
                
if __name__ == "__main__":
    fillJsonDB()