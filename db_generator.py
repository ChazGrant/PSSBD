import random
import string
from typing import List
import psycopg2
import datetime
import russian_names
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
    social_statuses = ["высший класс", "средний клас", "безработные", "студент", "иммигрант", "бездомный"]
    for social_status in social_statuses:
        cursor.execute("INSERT INTO social_status(social_status_name) VALUES(%s);", (social_status, ))

def fillProcedures(cursor) -> None:
    procedures = ["укол", "электрокардиограмма", "кислородная подушка", "таблетки"]
    # 6
    procedures = ["вентиляция лёгких", "измерение пульса", "остановка кровотечения", "кардиоверсия", "измерение уровня сахара", "измерение артериального давления"]
    for procedure in procedures:
        cursor.execute("INSERT INTO procedure(procedure_name) VALUES(%s);", (procedure, ))

def fillCallReasons(cursor) -> None:
    call_reasons = ["высокая температура", "сердечный приступ", "головная боль", "высокое давление", "боль в животе"]
    call_reasons = ["судороги", "слабость", "подозрение на инсульт", "отёк", "отравление"]
    for call_reason in call_reasons:
        cursor.execute("INSERT INTO call_reason(call_reason_name) VALUES(%s);", (call_reason, ))

def fillSickPeople(cursor, conn) -> None:
    for i in range(30000):
        batch_data = list()
        sql = "INSERT INTO sick_people(full_name, birth_date, social_status_id, phone_number, address) VALUES"
        for ii in range(1000):
            full_name = russian_names.RussianNames().get_person()
            birth_date = generateRandomBirthDate()
            social_status_id = random.randint(5, 8)
            phone_number = generateRandomPhoneNumber()
            address = generateRandomAddress()

            batch_data.append([full_name, birth_date, social_status_id, phone_number, address])

            if (ii + 1) % 250 == 0:
                print(ii + 1)
        
        for items in batch_data:
            sql += "(" + ", ".join([f"'{item}'" for item in items]) + "), "

        sql = sql[:-2] + ";"

        cursor.execute(sql)
        conn.commit()

        print("%d/29000" % ((i + 1) * 1000))
        print()

def fillCallRequests(cursor, conn) -> None:
    for i in range(0, 24001, 1000):
        batch_data = list()
        sql = "INSERT INTO call_requests(sick_people_id, call_date_time, call_reason_id, money_payment) VALUES"
        for ii in range(1000):
            sick_people_id = getRandomSickPeopleId(cursor)
            call_date_time = getRandomCallDateTime()
            call_reason_id = random.randint(2, 6)
            money_payment = generateRandomEquivalent()

            batch_data.append([sick_people_id, call_date_time, call_reason_id, money_payment])
            if (ii + 1) % 250 == 0:
                print(ii + 1)
        
        for items in batch_data:
            sql += "(" + ", ".join([f"'{item}'" for item in items]) + "), "

        sql = sql[:-2] + ";"

        cursor.execute(sql)
        conn.commit()

        print("%d/30000" % ((i) ))
        print()

def fillFirstAidStations(cursor, conn) -> None:
    for i in range(30):
        batch_data = list()
        sql = "INSERT INTO first_aid_stations(first_aid_station_number, city_district, employees_amount, phone_number, address) VALUES"
        cursor.execute("SELECT first_aid_station_number FROM first_aid_stations;")
        station_numbers = [item[0] for item in cursor.fetchall()]
        for ii in range(1000):
            while True:
                first_aid_station_number = random.randint(1, 99999)
                if first_aid_station_number not in station_numbers:
                    station_numbers.append(first_aid_station_number)
                    break
            city_district = random.choice(CITY_DISTRICTS)
            employees_amount = random.randint(150, 300)
            phone_number = generateRandomPhoneNumber()
            address = generateRandomAddress()
            
            batch_data.append([first_aid_station_number, city_district, employees_amount, phone_number, address])
            if (ii + 1) % 250 == 0:
                print(ii + 1)
        
        for items in batch_data:
            sql += "(" + ", ".join([f"'{item}'" for item in items]) + "), "

        sql = sql[:-2] + ";"

        cursor.execute(sql)
        conn.commit()

        print("%d/30000" % ((i + 1) * 1000) )
        print()

def getRandomProcedureId(cursor) -> int:
    cursor.execute("SELECT COUNT(*) FROM procedure;")
    procedures_amount = int(cursor.fetchone()[0])

    random_offset = random.randint(0, procedures_amount - 1)
    cursor.execute(f"SELECT procedure_id FROM procedure OFFSET {random_offset} LIMIT 1;")
    return int(cursor.fetchone()[0])

def getAllCallRequests(cursor) -> List[int]:
    cursor.execute("SELECT call_request_id FROM call_requests;")
    return [int(item[0]) for item in cursor.fetchall()]

def fillProcedureApplication(cursor, conn) -> None:
    call_requests_id = getAllCallRequests(cursor)
    sql = "INSERT INTO procedure_application(application_id, procedure_id) VALUES"
    batch_data = list()
    for idx, call_request_id in enumerate(call_requests_id):
        procedures_amount = random.randint(1, 4)
        procedures_id = []
        while True:
            procedure_id = random.randint(2, 5)
            if procedure_id in procedures_id:
                continue

            procedures_id.append(procedure_id)
            if len(procedures_id) == procedures_amount:
                break
        for proc_id in procedures_id:
            batch_data.append([call_request_id, proc_id])

        if (idx + 1) % 500 == 0:
            print(idx + 1)
    
    for items in batch_data:
        sql += "(" + ", ".join([str(item) for item in items]) + "), "

    sql = sql[:-2] + ";"

    cursor.execute(sql)
    conn.commit()


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
    fillCallReasons(cursor)
    conn.commit()

if __name__ == "__main__":
    main()
    # database = generateRandomDatabase(10, 20, 30)
    # print(database)
