import psycopg2
# from CONFIG import CONFIG


# conn = psycopg2.connect(**CONFIG)
# cursor = conn.cursor()

# итоговый запрос без условия; 
# итоговый запрос с условием на данные; 
# итоговый запрос с условием на группы; 
# итоговый запрос с условием на данные и на группы;
# запрос на запросе по принципу итогового запроса;
# запрос с подзапросом.
def totalQueryWithoutCondition(cursor):
    cursor.execute("SELECT SUM(money_payment) as total_payment FROM call_requests")

def totalQueryWithDataCondition(cursor):
    cursor.execute("SELECT SUM(money_payment) as total_payment FROM call_requests WHERE call_reason_id=%s")

def totalQueryWithGroupCondition(cursor):
    cursor.execute("SELECT cr.call_reason_name, SUM(money_payment) AS total_payment FROM call_requests \
        INNER JOIN call_reason cr ON call_requests.call_reason_id=cr.call_reason_id \
        GROUP BY cr.call_reason_name;")

def totalQueryWithDataGroupCondition(cursor):
    cursor.execute("SELECT cr.call_reason_name, SUM(money_payment) AS total_payment FROM call_requests \
        INNER JOIN call_reason cr ON call_requests.call_reason_id=cr.call_reason_id \
            WHERE call_requests.call_reason_id IN (%s, %s) \
            GROUP BY cr.call_reason_name;")

def queryOnTotalQuery(cursor):
    cursor.execute("SELECT call_date_time, money_payment FROM call_requests WHERE money_payment > \
        (SELECT AVG(money_payment) FROM call_requests) LIMIT 10;")

def totalQueryWithSubquery(cursor):
    cursor.execute("SELECT call_date_time, money_payment FROM call_requests WHERE money_payment > \
        (SELECT money_payment FROM call_requests LIMIT 1) LIMIT 10;")

if __name__ == "__main__":
    totalQueryWithoutCondition()
    totalQueryWithDataCondition()
    totalQueryWithGroupCondition()
    totalQueryWithDataGroupCondition()
    queryOnTotalQuery()
    totalQueryWithSubquery()
