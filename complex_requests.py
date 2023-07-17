import psycopg2
from CONFIG import CONFIG


conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()

# итоговый запрос без условия; 
# итоговый запрос с условием на данные; 
# итоговый запрос с условием на группы; 
# итоговый запрос с условием на данные и на группы;
# запрос на запросе по принципу итогового запроса;
# запрос с подзапросом.
def totalQueryWithoutCondition():
    cursor.execute("SELECT SUM(money_payment) as total_payment FROM call_requests")
    data = cursor.fetchone()[0]
    print(data)

def totalQueryWithDataCondition():
    cursor.execute("SELECT SUM(money_payment) as total_payment FROM call_requests WHERE call_reason_id=5")
    data = cursor.fetchone()[0]
    print(data)

def totalQueryWithGroupCondition():
    cursor.execute("SELECT cr.call_reason_name, SUM(money_payment) AS total_payment FROM call_requests \
        INNER JOIN call_reason cr ON call_requests.call_reason_id=cr.call_reason_id \
        GROUP BY cr.call_reason_name;")
    data = cursor.fetchall()
    print(data)

def totalQueryWithDataGroupCondition():
    cursor.execute("SELECT cr.call_reason_name, SUM(money_payment) AS total_payment FROM call_requests \
        INNER JOIN call_reason cr ON call_requests.call_reason_id=cr.call_reason_id \
            WHERE call_requests.call_reason_id IN (2, 4) \
            GROUP BY cr.call_reason_name;")
    data = cursor.fetchall()
    print(data)

def queryOnTotalQuery():
    cursor.execute("SELECT call_date_time, money_payment FROM call_requests WHERE money_payment > \
        (SELECT AVG(money_payment) FROM call_requests) LIMIT 10;")
    data = cursor.fetchall()
    for item in data:
        print(item)

def totalQueryWithSubquery():
    cursor.execute("SELECT call_date_time, money_payment FROM call_requests WHERE money_payment > \
        (SELECT money_payment FROM call_requests LIMIT 1) LIMIT 10;")
    data = cursor.fetchall()
    for item in data:
        print(item)

if __name__ == "__main__":
    totalQueryWithoutCondition()
    totalQueryWithDataCondition()
    totalQueryWithGroupCondition()
    totalQueryWithDataGroupCondition()
    queryOnTotalQuery()
    totalQueryWithSubquery()
