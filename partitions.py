# Партиция 1 - по хешу
# Партиция 2 - по диапазону
# Дополнительно - присоединение новой таблицы к патриции №2

import psycopg2
from CONFIG import CONFIG


conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()

def createFirstSectionTable():
    cursor.execute("CREATE TABLE hash_call_requests( \
                    \"hash_call_request_id\" SERIAL PRIMARY KEY NOT NULL, \
                    sick_people_id int4 NOT NULL, \
                    call_date_time TIMESTAMP NOT NULL, \
                    call_reason_id int4 NOT NULL, \
                    money_payment int4 NOT NULL) \
                    PARTITION BY HASH (\"id\");")
    cursor.execute("CREATE TABLE hash_call_requests_0 PARTITION OF hash_call_requests \
                   FOR VALUES WITH (MODULUS 4, REMINDER 0)")
    cursor.execute("CREATE TABLE hash_call_requests_1 PARTITION OF hash_call_requests \
                   FOR VALUES WITH (MODULUS 4, REMINDER 1)")
    cursor.execute("CREATE TABLE hash_call_requests_2 PARTITION OF hash_call_requests \
                   FOR VALUES WITH (MODULUS 4, REMINDER 2)")
    cursor.execute("CREATE TABLE hash_call_requests_3 PARTITION OF hash_call_requests \
                   FOR VALUES WITH (MODULUS 4, REMINDER 3)")

def createSecondSectionTable():
    ...

def createSimpleTable():
    ...

def copyDataFromFirstPartition():
    ...

def createIndexByPartitionKeyFirstSectionTable():
    cursor.execute("CREATE INDEX ON hash_call_requests(\"id\");")

def createIndexByPartitionKeySecondSectionTable():
    ...

def createIndexByKeyFieldOneFirstSectionTable():
    ...

def createIndexByKeyFieldOneSecondSectionTable():
    ...

def createIndexByKeyFieldTwoFirstSectionTable():
    ...

def createIndexByKeyFieldTwoSecondSectionTable():
    ...

def explainOne():
    ...

def explainTwo():
    ...

if __name__ == "__main__":
    ...
