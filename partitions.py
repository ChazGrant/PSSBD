# Партиция 1 - по хешу
# Партиция 2 - по диапазону
# Дополнительно - присоединение новой таблицы к патриции №2

import psycopg2
from CONFIG import CONFIG


conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()

def _createFirstSectionTable():
    cursor.execute("DROP TABLE IF EXISTS hash_call_requests")
    cursor.execute("CREATE TABLE hash_call_requests( \
                    \"hash_call_requests_id\" SERIAL PRIMARY KEY NOT NULL, \
                    sick_people_id int4 NOT NULL, \
                    call_date_time TIMESTAMP NOT NULL, \
                    call_reason_id int4 NOT NULL, \
                    money_payment int4 NOT NULL) \
                    PARTITION BY HASH (\"hash_call_requests_id\")")
    
    cursor.execute("CREATE TABLE hash_call_requests_hash0 PARTITION OF hash_call_requests \
	FOR VALUES WITH (MODULUS 4, REMAINDER 0);")
    cursor.execute("CREATE TABLE hash_call_requests_hash1 PARTITION OF hash_call_requests \
	FOR VALUES WITH (MODULUS 4, REMAINDER 1);")
    cursor.execute("CREATE TABLE hash_call_requests_hash2 PARTITION OF hash_call_requests \
	FOR VALUES WITH (MODULUS 4, REMAINDER 2);")
    cursor.execute("CREATE TABLE hash_call_requests_hash3 PARTITION OF hash_call_requests \
	FOR VALUES WITH (MODULUS 4, REMAINDER 3);")

    conn.commit()

def createIndexByPartitionKeyFirstSectionTable():
    cursor.execute("CREATE INDEX ON hash_call_requests(\"hash_call_requests_id\");")
    conn.commit()

def createIndexByKeyFieldOneFirstSectionTable():
    cursor.execute("CREATE INDEX ON hash_call_requests(\"sick_people_id\");")
    conn.commit()

def createIndexByKeyFieldTwoFirstSectionTable():
    cursor.execute("CREATE INDEX ON hash_call_requests(\"call_date_time\");")
    conn.commit()

def fillFirstSectionTable(month: str, sign='-'):
    cursor.execute(f"INSERT INTO hash_call_requests (sick_people_id, call_date_time, \
                   call_reason_id, money_payment) SELECT \
                                    trunc(random() * 999999), \
                                    now() {sign}{month}::interval * random(), \
                                    trunc(random() * 25), \
                                    trunc(random() * 2500 + 500) \
                   FROM generate_series(1, 100000)")
    conn.commit()

def _createSecondSectionTable():
    cursor.execute("DROP TABLE IF EXISTS range_call_requests")
    cursor.execute("CREATE TABLE range_call_requests( \
                    \"range_call_request_id\" SERIAL NOT NULL, \
                    sick_people_id int4 NOT NULL, \
                    call_date_time TIMESTAMP NOT NULL, \
                    call_reason_id int4 NOT NULL, \
                    money_payment int4 NOT NULL) \
                    PARTITION BY RANGE (\"call_date_time\");")
    
    cursor.execute("CREATE TABLE range_call_requests_0 PARTITION OF range_call_requests \
                   FOR VALUES FROM ('2022-07-01') TO ('2022-10-01')")
    
    cursor.execute("CREATE TABLE range_call_requests_1 PARTITION OF range_call_requests \
                   FOR VALUES FROM ('2022-10-01') TO ('2023-01-01')")
    
    cursor.execute("CREATE TABLE range_call_requests_2 PARTITION OF range_call_requests \
                   FOR VALUES FROM ('2023-01-01') TO ('2023-04-01')")
    
    cursor.execute("CREATE TABLE range_call_requests_3 PARTITION OF range_call_requests \
                   FOR VALUES FROM ('2023-04-01') TO ('2023-07-01')")
    
    cursor.execute("CREATE TABLE range_call_requests_default PARTITION OF range_call_requests \
                   DEFAULT")
    
    conn.commit()

def createIndexByPartitionKeySecondSectionTable():
    cursor.execute("CREATE INDEX ON range_call_requests(\"call_date_time\");")
    conn.commit()

def createIndexByKeyFieldOneSecondSectionTable():
    cursor.execute("CREATE INDEX ON range_call_requests(\"sick_people_id\");")
    conn.commit()

def createIndexByKeyFieldTwoSecondSectionTable():
    cursor.execute("CREATE INDEX ON range_call_requests(\"call_reason_id\");")
    conn.commit()

def copyDataFromFirstSectionTableFirstPartitionToSecondSectionTable():
    cursor.execute("INSERT INTO range_call_requests SELECT * FROM hash_call_requests_hash0")
    conn.commit()

def createSimpleTable():
    cursor.execute("CREATE TABLE call_requests_copy( \
                    \"call_request_id\" SERIAL PRIMARY KEY NOT NULL, \
                    sick_people_id int4 NOT NULL, \
                    call_date_time TIMESTAMP NOT NULL, \
                    call_reason_id int4 NOT NULL, \
                    money_payment int4 NOT NULL);")
    conn.commit()

def createIndexByKeyFieldOneCopyTable():
    cursor.execute("CREATE INDEX ON call_requests_copy(\"sick_people_id\")")
    conn.commit()

def createIndexByKeyFieldTwoCopyTable():
    cursor.execute("CREATE INDEX ON call_requests_copy(\"call_reason_id\")")
    conn.commit()

def copyDataFromFirstSectionTableFirstPartitionToSimpleTable():
    cursor.execute("INSERT INTO call_requests_copy SELECT * FROM hash_call_requests_hash0")
    conn.commit()

def explainFirstSectionTableAndCopyTable():
    cursor.execute("EXPLAIN(ANALYZE) SELECT * FROM hash_call_requests \
                    WHERE call_date_time >= '2022-10-01' ORDER BY hash_call_requests_id")
    print(cursor.fetchall())
    print()
    cursor.execute("EXPLAIN(ANALYZE) SELECT * FROM call_requests_copy \
                    WHERE call_date_time >= '2022-10-01' ORDER BY call_request_id")
    print(cursor.fetchall())

def explainSecondSectionTableAndCopyTable():
    cursor.execute("EXPLAIN(ANALYZE) SELECT * FROM range_call_requests \
                    WHERE call_date_time >= '2022-10-01' ORDER BY call_date_time")
    print(cursor.fetchall())
    print()
    cursor.execute("EXPLAIN(ANALYZE) SELECT * FROM call_requests_copy \
                    WHERE call_date_time >= '2022-10-01' ORDER BY call_date_time")
    print(cursor.fetchall())

def firstSectionTableCreation():
    _createFirstSectionTable()
    createIndexByKeyFieldOneFirstSectionTable()
    createIndexByKeyFieldTwoFirstSectionTable()
    createIndexByPartitionKeyFirstSectionTable()
    fillFirstSectionTable('- 3 \'month\'')
    fillFirstSectionTable('\'8 month\'')
    fillFirstSectionTable('\'6 month\'')
    fillFirstSectionTable('\'2 month\'')
    fillFirstSectionTable('\'2 month\'', '+')

def secondSectionTableCreation():
    _createSecondSectionTable()
    createIndexByPartitionKeySecondSectionTable()
    createIndexByKeyFieldOneSecondSectionTable()
    createIndexByKeyFieldTwoSecondSectionTable()
    copyDataFromFirstSectionTableFirstPartitionToSecondSectionTable()

def simpleTableCreation():
    createSimpleTable()
    createIndexByKeyFieldOneCopyTable()
    createIndexByKeyFieldTwoCopyTable()
    copyDataFromFirstSectionTableFirstPartitionToSimpleTable()


if __name__ == "__main__":
    # simpleTableCreation()
    explainFirstSectionTableAndCopyTable()
    explainSecondSectionTableAndCopyTable()
