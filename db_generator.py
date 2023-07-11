import random
import string
from typing import List
import psycopg2
import datetime
from CONFIG import CONFIG


CITY_DISTRICTS = ["Восточный округ", "Западный округ", "Ленинский", "Октябрьский", "Центральный", "Краснооктябрьский"
"Падунский", "Правобережный", "Фокинский", "Первореченский", "Затеречный", "Кировский", "Красноармейский"]

def generateRandomName() -> str:
    first_names = ["Доброжир", "Тихомир", "Ратибор", "Путислав", "Ярополк", "Гостомысл", "Велимудр", "Святослав"]
    last_names = ["Адамич", "Антич", "Бабич", "Богданич", "Броз", "Црнчевич", "Драгович", "Филипович", "Франич", "Франич", "Грбич", "Гргич", "Хорват", "Илич", "Иванович", "Янкович", "Лончар", "Петрич"]
    return random.choice(first_names) + " " + random.choice(last_names)

def generateRandomBirthDate() -> datetime.date:
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1950, 2000)
    return datetime.date(year, month, day)

def generateRandomAddress() -> str:
    streets = ["Main Street", "Park Avenue", "First Street", "Elm Street", "Maple Avenue"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    return f"{random.randint(1, 999)} {random.choice(streets)}, {random.choice(cities)}"

def getRandomSocialStatusId(cursor) -> None:
    cursor.execute("SELECT COUNT(*) FROM social_status")
    statuses_amount = cursor.fetchone()[0]
    random_offset = random.randint(0, statuses_amount - 1)

    cursor.execute(f"SELECT social_status_id FROM social_status OFFSET {random_offset} LIMIT 1;")
    return cursor.fetchone()[0]

def getRandomSickPeopleId(cursor) -> int:
    cursor.execute("SELECT COUNT(*) FROM sick_people")
    people_amount = int(cursor.fetchone()[0])

    random_offset = random.randint(0, people_amount - 1)
    cursor.execute(f"SELECT sick_people_id FROM sick_people OFFSET {random_offset} LIMIT 1;")
    return int(cursor.fetchone()[0])

def getRandomCallDateTime() -> datetime.datetime:
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(2017, 2023)
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)
    return datetime.datetime(year, month, day, hours, minutes, seconds)

def getRandomCallReasonId(cursor) -> int:
    cursor.execute("SELECT COUNT(*) FROM call_reason;")
    call_reason_amount = int(cursor.fetchone()[0])

    random_offset = random.randint(0, call_reason_amount - 1)
    cursor.execute(f"SELECT call_reason_id FROM call_reason OFFSET {random_offset} LIMIT 1;")
    return int(cursor.fetchone()[0])

def fillSocialStatuses(cursor) -> None:
    social_statuses = ["пенсионер", "рабочий", "служащий", "предприниматель"]
    for social_status in social_statuses:
        cursor.execute("INSERT INTO social_status(social_status_name) VALUES('%s');", (social_status, ))

def fillProcedures(cursor) -> None:
    procedures = ["укол", "электрокардиограмма", "кислородная подушка", "таблетки"]
    for procedure in procedures:
        cursor.execute("INSERT INTO procedure(procedure_name) VALUES('%s');", (procedure, ))

def fillCallReasons(cursor) -> None:
    call_reasons = ["высокая температура", "сердечный приступ", "головная боль", "высокое давление", "боль в животе"]
    for call_reason in call_reasons:
        cursor.execute("INSERT INTO call_reason(call_reason_name) VALUES(%s);", (call_reason, ))

def fillSickPeople(cursor) -> None:
    for _ in range(50):
        full_name = generateRandomName()
        birth_date = generateRandomBirthDate()
        social_status_id = getRandomSocialStatusId(cursor)
        phone_number = generateRandomPhoneNumber()
        address = generateRandomAddress()

        cursor.execute("INSERT INTO sick_people(full_name, birth_date, social_status_id, phone_number, address) \
            VALUES (%s, %s, %s, %s, %s);", (full_name, birth_date, social_status_id, phone_number, address))

def fillCallRequests(cursor) -> None:
    for _ in range(50):
        sick_people_id = getRandomSickPeopleId(cursor)
        call_date_time = getRandomCallDateTime()
        call_reason_id = getRandomCallReasonId(cursor)
        money_payment = generateRandomEquivalent()

        cursor.execute("INSERT INTO call_requests(sick_people_id, call_date_time, call_reason_id, money_payment) \
            VALUES (%s, %s, %s, %s);", (sick_people_id, call_date_time, call_reason_id, money_payment))

def fillFirstAidStations(cursor) -> None:
    for _ in range(50):
        first_aid_station_number = random.randint(1000, 9999)
        city_district = random.choice(CITY_DISTRICTS)
        employees_amount = random.randint(250, 300)
        phone_number = generateRandomPhoneNumber()
        address = generateRandomAddress()
        
        cursor.execute("INSERT INTO first_aid_stations(first_aid_station_number, city_district, employees_amount, phone_number, address) \
            VALUES (%s, %s, %s, %s, %s);", (first_aid_station_number, city_district, employees_amount, phone_number, address))

def getRandomProcedureId(cursor) -> int:
    cursor.execute("SELECT COUNT(*) FROM procedure;")
    procedures_amount = int(cursor.fetchone()[0])

    random_offset = random.randint(0, procedures_amount - 1)
    cursor.execute(f"SELECT procedure_id FROM procedure OFFSET {random_offset} LIMIT 1;")
    return int(cursor.fetchone()[0])

def getAllCallRequests(cursor) -> List[int]:
    cursor.execute("SELECT call_request_id FROM call_requests;")
    return [int(item[0]) for item in cursor.fetchall()]

def fillProcedureApplication(cursor) -> None:
    call_requests_id = getAllCallRequests(cursor)
    for call_request_id in call_requests_id[1:]:
        procedures_amount = random.randint(1, 4)
        procedures_id = []
        while True:
            procedure_id = getRandomProcedureId(cursor)
            if procedure_id in procedures_id:
                continue

            procedures_id.append(procedure_id)
            if len(procedures_id) == procedures_amount:
                break
        
        for procedure_id in procedures_id:
            cursor.execute("INSERT INTO procedure_application(application_id, procedure_id) VALUES (%s, %s);",
            (call_request_id, procedure_id))

def generateRandomPhoneNumber() -> str:
    return ''.join(random.choice(string.digits) for _ in range(10))

def generateRandomCallReason() -> str:
    reasons = ["высокая температура", "сердечный приступ", "головная боль", "высокое давление", "боль в животе"]
    return random.choice(reasons)

def generateRandomProcedure() -> str:
    procedures = ["укол", "электрокардиограмма", "кислородная подушка", "таблетки"]
    return random.choice(procedures)

def generateRandomEquivalent() -> int:
    return random.randint(500, 3000)

def main():
    conn = psycopg2.connect(**CONFIG)
    cursor = conn.cursor()

    fillProcedureApplication(cursor)
    conn.commit()

if __name__ == "__main__":
    main()
    # database = generateRandomDatabase(10, 20, 30)
    # print(database)
