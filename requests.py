import psycopg2
from CONFIG import CONFIG


# симметричное внутреннее соединение с условием (два запроса с условием отбора по внешнему ключу, два – по датам); 
# симметричное внутреннее соединение без условия (три запроса); 
# левое внешнее соединение; 
# правое внешнее соединение;
# запрос на запросе по принципу левого ссоединения;

conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()

def symmetricInnerRequestWithConditionExternalKeyOne():
    cursor.execute("SELECT sp.full_name, sp.birth_date, sc.social_status_name FROM sick_people sp\
                   INNER JOIN social_status sc ON sp.social_status_id=sc.social_status_id \
<<<<<<< HEAD
                   WHERE sc.social_status_name=%s", ("пенсионер", ))
=======
                   WHERE sp.social_status_name=%s LIMIT 10;", ("рабочий", ))
>>>>>>> eb80c48660e6d68890fe24061ce7b2708e551dde
    items = cursor.fetchall()
    print(items)

def symmetricInnerRequestWithConditionExternalKeyTwo():
    cursor.execute("SELECT sp.full_name, cr.call_date_time, cr.money_payment FROM call_requests cr \
                   INNER JOIN sick_people sp ON sp.sick_people_id=cr.sick_people_id \
<<<<<<< HEAD
                   WHERE sp.full_name=%s", ("Вероника Петровна Кнепская", ))
=======
                   WHERE sp.full_name LIKE %s LIMIT 10;", ("Вер%", ))
>>>>>>> eb80c48660e6d68890fe24061ce7b2708e551dde
    items = cursor.fetchall()
    print(items)

def symmetricInnerRequestWithConditionDateOne():
    cursor.execute("SELECT sp.full_name, cr.call_date_time, cr.money_payment FROM call_requests cr \
                   INNER JOIN sick_people sp ON sp.sick_people_id=cr.sick_people_id \
                   WHERE cr.call_date_time > %s LIMIT 10;", ('2021-09-22', ))
    items = cursor.fetchall()
    for item in items:
        print(item)

def symmetricInnerRequestWithConditionDateTwo():
    cursor.execute("SELECT sp.full_name, cr.call_date_time, cr.money_payment FROM call_requests cr \
                   INNER JOIN sick_people sp ON sp.sick_people_id=cr.sick_people_id \
                   WHERE cr.call_date_time BETWEEN %s AND %s LIMIT 10;", ('2022-01-01', '2022-12-31'))
    items = cursor.fetchall()
    for item in items:
        print(item)

def symmetricInnerRequestWithoutConditionOne():
    cursor.execute("SELECT sp.full_name, cr.call_date_time, car.call_reason_name, cr.money_payment \
                   FROM call_requests cr \
                   INNER JOIN sick_people sp ON sp.sick_people_id=cr.sick_people_id \
                   INNER JOIN call_reason car ON cr.call_reason_id=car.call_reason_id \
                   LIMIT 10;")
    items = cursor.fetchall()
    for item in items:
        print(item)

def symmetricInnerRequestWithoutConditionTwo():
    cursor.execute("SELECT cr.money_payment, p.procedure_name \
                   FROM procedure_application pa \
                   INNER JOIN call_requests cr ON cr.call_request_id=pa.application_id \
                   INNER JOIN procedure p ON p.procedure_id=pa.procedure_id \
                   LIMIT 10;")
    items = cursor.fetchall()
    for item in items:
        print(item)

def symmetricInnerRequestWithoutConditionThree():
    cursor.execute("SELECT sp.full_name, sp.birth_date, ss.social_status_name, sp.phone_number, sp.address \
                   FROM sick_people sp \
                   INNER JOIN social_status ss ON sp.social_status_id=ss.social_status_id \
                   LIMIT 10;")
    items = cursor.fetchall()
    for item in items:
        print(item)

def leftOuterJoinRequest():
    cursor.execute("SELECT ss.social_status_name, sp.birth_date\
                   FROM social_status ss \
                   LEFT JOIN sick_people sp ON sp.social_status_id=ss.social_status_id \
                   LIMIT 10;")
    items = cursor.fetchall()
    for item in items:
        print(item)

def rightOuterJoinRequest():
    cursor.execute("SELECT crea.call_reason_name, creq.money_payment \
                   FROM call_reason crea \
                   RIGHT JOIN call_requests creq ON crea.call_reason_id=creq.call_reason_id \
                   LIMIT 10;")
    items = cursor.fetchall()
    for item in items:
        print(item)

def requestOnRequestLeftJoin():
    cursor.execute("SELECT full_name, phone_number FROM sick_people \
                   WHERE social_status_id in (SELECT ss.social_status_id\
                   FROM social_status ss \
                   LEFT JOIN sick_people sp ON sp.social_status_id=ss.social_status_id \
                   WHERE sp.birth_date > %s) LIMIT 10;", ('1995-01-01', ))
    items = cursor.fetchall()
    for item in items:
        print(item)


if __name__ == "__main__":
    symmetricInnerRequestWithConditionExternalKeyTwo()