from CONFIG import CONFIG
import psycopg2


json_example = {
    "call_reason_name": "value",
    "sick_person": {
        "name": "Данил",
        "surname": "Шустов",
        "age": 23,
        "gender": 1,
        "credentials": {
            "passport_series": "22 34",
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

conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()

def queryWithConcreteFieldsOutputOne():
    cursor.execute("SELECT call_request_json_data ->> 'call_reason_name' as call_reason, \
                           call_request_json_data ->> 'money_payment' as money_ \
                    FROM json_call_requests \
                    WHERE call_request_json_data ->> 'money_payment' = '500';")
    data = cursor.fetchall()
    print(data)

def queryWithConcreteFieldsOutputTwo():
    cursor.execute("SELECT call_request_json_data ->> 'call_reason_name' as call_reason, \
                           call_request_json_data ->> 'money_payment' as money, \
                           call_request_json_data -> 'sick_person' ->> 'gender', \
                           call_request_json_data -> 'sick_person' -> 'credentials' ->> 'passport_series' \
                    FROM json_call_requests \
                    WHERE call_request_json_data -> 'sick_person' ->> 'gender' = '1';")
    data = cursor.fetchall()
    print(data)

def queryWithConcreteFieldsOutputThree():
    cursor.execute("SELECT call_request_json_data ->> 'call_reason_name' as call_reason, \
                           call_request_json_data ->> 'money_payment' as money, \
                           (call_request_json_data -> 'sick_person' ->> 'gender')::int as gender, \
                           call_request_json_data -> 'sick_person' -> 'credentials' ->> 'passport_series' as passport_series \
                    FROM json_call_requests \
                    WHERE (call_request_json_data -> 'sick_person' ->> 'age')::int > 30;")
    data = cursor.fetchall()
    print(data)

def jsonpathQueryOne():
    cursor.execute("SELECT call_request_json_data -> 'sick_person' ->> 'name' as name, \
                           call_request_json_data ->> 'call_reason_name' as call_reason, \
                           call_request_json_data ->> 'money_payment' as money, \
                           call_request_json_data -> 'sick_person' ->> 'gender', \
                           call_request_json_data -> 'sick_person' -> 'credentials' -> 'additional_info' ->> 'country', \
                           call_request_json_data -> 'sick_person' -> 'credentials' -> 'additional_info' ->> 'city' \
                    FROM json_call_requests \
                    WHERE call_request_json_data @@ '$.sick_person[*].name == \"Валентина\"';")
    data = cursor.fetchall()
    print(data)

def jsonpathQueryTwo():
    cursor.execute("SELECT call_request_json_data -> 'sick_person' ->> 'name' as name, \
                           call_request_json_data ->> 'call_reason_name' as call_reason, \
                           call_request_json_data ->> 'money_payment' as money, \
                           call_request_json_data -> 'sick_person' ->> 'gender', \
                           call_request_json_data -> 'sick_person' -> 'credentials' -> 'additional_info' ->> 'country', \
                           call_request_json_data -> 'sick_person' -> 'credentials' -> 'additional_info' ->> 'city' \
                    FROM json_call_requests \
                    WHERE call_request_json_data @@ 'exists($.sick_person[*] ? (@.name == \"Валентина\") ? (@.age > 30))';")
    data = cursor.fetchall()
    print(data)

def jsonpathQueryThree():
    cursor.execute("SELECT call_request_json_data -> 'sick_person' ->> 'name' as name, \
                           call_request_json_data ->> 'call_reason_name' as call_reason, \
                           call_request_json_data ->> 'money_payment' as money, \
                           call_request_json_data -> 'sick_person' ->> 'gender', \
                           call_request_json_data -> 'sick_person' -> 'credentials' -> 'additional_info' ->> 'country', \
                           call_request_json_data -> 'sick_person' -> 'credentials' -> 'additional_info' ->> 'city' \
                    FROM json_call_requests \
                    WHERE jsonb_path_exists(call_request_json_data, '$.sick_person[*] ? (@.name == \"Валентина\") ? (@.age > 30)');")
    data = cursor.fetchall()
    print(data)

def queryWithProcessingFunctionOne():
    cursor.execute("SELECT * \
                   FROM jsonb_populate_recordset(null::record, \
                   (SELECT jsonb_path_query_array(call_request_json_data, '$.sick_person[*]') \
                   FROM json_call_requests \
                   WHERE call_request_json_data->>'call_date_time' = '2018-12-01 21:41:02') \
                   ) AS (\"name\" varchar, \"surname\" varchar, \"age\" integer, \"gender\" integer);")
    data = cursor.fetchall()
    print(data)

def queryWithProcessingFunctionTwo():
    cursor.execute("SELECT * \
                   FROM jsonb_populate_record(null::record, \
                   (SELECT jsonb_path_query(call_request_json_data, '$.sick_person[*]?(@.age == 40)') \
                   FROM json_call_requests \
                   WHERE call_request_json_data->>'call_date_time' = '2018-12-01 21:41:02') \
                   ) AS (\"name\" varchar, \"surname\" varchar, \"age\" integer, \"gender\" integer);")
    data = cursor.fetchall()
    print(data)

def queryWithProcessingFunctionThree():
    cursor.execute("SELECT jsonb_each_text( \
                   jsonb_path_query(call_request_json_data, '$.sick_person[*]?(@.age == 40)')) \
                   FROM json_call_requests \
                   WHERE jsonb_path_match( \
                   call_request_json_data, 'exists($.sick_person[*].credentials.additional_info.city ? (@ == \"New York\"))')")
    data = cursor.fetchall()
    print(data)

def addDataQueryOne():
    cursor.execute("UPDATE json_call_requests \
                    SET call_request_json_data = jsonb_insert(call_request_json_data, \
                    '{passport_overdue}', '1') \
                    WHERE jsonb_path_exists(call_request_json_data, '$.sick_person[*] ? (@.age == 53)') RETURNING *;")
    print(cursor.fetchall())
    conn.commit()

def addDataQueryTwo():
    cursor.execute("UPDATE json_call_requests \
                    SET call_request_json_data = call_request_json_data || '{\"call_cancelled\": \"1\"}' \
                    WHERE jsonb_path_exists(call_request_json_data, '$.sick_person[*] ? (@.age > 60) ? (@.gender == 1)') RETURNING *;")
    print(cursor.fetchall())
    conn.commit()

def updateDataQueryOne():
    cursor.execute("UPDATE json_call_requests \
                    SET call_request_json_data = jsonb_set(call_request_json_data, '{call_cancelled}', '0')  \
                    WHERE jsonb_path_exists(call_request_json_data, '$.sick_person[*] ? (@.age > 60) ? (@.gender == 1)') RETURNING *;")
    print(cursor.fetchall())
    conn.commit()

def updateDataQueryTwo():
    cursor.execute("UPDATE json_call_requests \
                    SET call_request_json_data = jsonb_set(call_request_json_data, '{passport_overdue}', '0')  \
                    WHERE (call_request_json_data -> 'sick_person' ->> 'age')::int > 50 \
                    AND (call_request_json_data -> 'sick_person' ->> 'age')::int < 55 \
                    RETURNING call_request_json_data;")
    print(cursor.fetchall())
    conn.commit()

def deleteDataQueryOne():
    cursor.execute("UPDATE json_call_requests \
                    SET call_request_json_data = call_request_json_data - 'call_cancelled' \
                    WHERE jsonb_path_exists(call_request_json_data, '$.sick_person[*] ? (@.age > 60 && @.age < 63) ? (@.gender == 1)') RETURNING call_request_json_data;")
    print(cursor.fetchall())
    conn.commit()

def deleteDataQueryTwo():
    cursor.execute("UPDATE json_call_requests \
                    SET call_request_json_data = call_request_json_data - 'passport_overdue' \
                    RETURNING call_request_json_data;")
    print(cursor.fetchall())
    conn.commit()

def deleteRecordQueryOne():
    cursor.execute("SELECT COUNT(*) FROM json_call_requests")
    print(cursor.fetchone()[0])

    cursor.execute("DELETE FROM json_call_requests \
                   WHERE call_request_json_data ->> 'call_cancelled' = '1'")
    
    cursor.execute("SELECT COUNT(*) FROM json_call_requests")
    print(cursor.fetchone()[0])
    # conn.commit()

def deleteRecordQueryTwo():
    cursor.execute("SELECT COUNT(*) FROM json_call_requests")
    print(cursor.fetchone()[0])

    cursor.execute("DELETE FROM json_call_requests \
                    WHERE jsonb_path_match(call_request_json_data, \
                    'exists($.sick_person[*] ? (@.name == \"Алина\"))');")
    
    cursor.execute("SELECT COUNT(*) FROM json_call_requests")
    print(cursor.fetchone()[0])
    # conn.commit()

"""
CREATE INDEX json_table_data_jsonb_idx ON json_table 
USING GIN (data_jsonb);
CREATE INDEX json_table_data_jsonb_dogovor_idx ON json_table 
USING GIN ((data_jsonb-> 'dogovor'));
CREATE INDEX json_table_data_jsonb_name_idx ON json_table 
USING GIN ((data_jsonb-> 'name'));
"""
def createIndexByFieldContainingJSONDoc():
    cursor.execute("CREATE INDEX json_call_requests_idx ON json_call_requests \
                   USING GIN (call_request_json_data)")
    conn.commit()

def createIndexByKeyElementOne():
    cursor.execute("CREATE INDEX sick_person_age_idx ON json_call_requests \
                        USING GIN ((call_request_json_data -> 'sick_person'));")
    conn.commit()


def createIndexByKeyElementTwo():
    cursor.execute("CREATE INDEX call_reason_name_idx ON json_call_requests \
                        USING GIN ((call_request_json_data -> 'call_reason_name'));")
    conn.commit()

def explainFunctionOne():
    cursor.execute("EXPLAIN(ANALYZE) SELECT call_request_json_data ->> 'call_reason_name' as call_reason, \
                   call_request_json_data ->> 'money_payment' as money_ \
                   FROM json_call_requests \
                   WHERE call_request_json_data ->> 'money_payment' = '500';")
    print(cursor.fetchall())
    cursor.execute("EXPLAIN(ANALYZE) SELECT call_request_json_data ->> 'call_reason_name' as call_reason, \
                           call_request_json_data ->> 'money_payment' as money_ \
                    FROM json_call_requests \
                    WHERE call_request_json_data @> '{\"money_payment\": \"500\"}';")
    print(cursor.fetchall())

def explainFunctionTwo():
    cursor.execute("EXPLAIN(ANALYZE) SELECT * \
                FROM jsonb_populate_recordset(null::record, \
                (SELECT jsonb_path_query_array(call_request_json_data, '$.sick_person[*]') \
                FROM json_call_requests \
                WHERE call_request_json_data->>'call_date_time' = '2018-12-01 21:41:02') \
                ) AS (\"name\" varchar, \"surname\" varchar, \"age\" integer, \"gender\" integer);")
    print(cursor.fetchall())

    cursor.execute("EXPLAIN(ANALYZE) SELECT * \
                FROM jsonb_populate_recordset(null::record, \
                (SELECT jsonb_path_query_array(call_request_json_data, '$.sick_person[*]') \
                FROM json_call_requests \
                WHERE call_request_json_data @> '{\"call_date_time\": \"2018-12-01 21:41:02\"}') \
                ) AS (\"name\" varchar, \"surname\" varchar, \"age\" integer, \"gender\" integer);")
    print(cursor.fetchall())

def explainFunctionThree():
    cursor.execute("SELECT jsonb_each_text( \
                   jsonb_path_query(call_request_json_data, '$.sick_person[*]?(@.age == 40)')) \
                   FROM json_call_requests \
                   WHERE jsonb_path_match( \
                   call_request_json_data, 'exists($.sick_person[*].credentials.additional_info.city ? (@ == \"New York\"))')")
    data = cursor.fetchall()
    print(data)

    cursor.execute("EXPLAIN(ANALYZE) SELECT * \
                FROM jsonb_populate_recordset(null::record, \
                (SELECT jsonb_path_query_array(call_request_json_data, '$.sick_person[*]') \
                FROM json_call_requests \
                WHERE call_request_json_data @> '{\"call_date_time\": \"2018-12-01 21:41:02\"}') \
                ) AS (\"name\" varchar, \"surname\" varchar, \"age\" integer, \"gender\" integer);")
    print(cursor.fetchall())

def explainFunctionFour():
    cursor.execute("SELECT jsonb_each_text( \
                   jsonb_path_query(call_request_json_data, '$.sick_person[*]?(@.age == 40)')) \
                   FROM json_call_requests \
                   WHERE jsonb_path_match( \
                   call_request_json_data, 'exists($.sick_person[*].credentials.additional_info.city ? (@ == \"New York\"))')")
    data = cursor.fetchall()
    print(data)

def explainFunctionFive():
    cursor.execute("SELECT * \
                   FROM jsonb_populate_record(null::record, \
                   (SELECT jsonb_path_query(call_request_json_data, '$.sick_person[*]?(@.age == 40)') \
                   FROM json_call_requests \
                   WHERE call_request_json_data->>'call_date_time' = '2018-12-01 21:41:02') \
                   ) AS (\"name\" varchar, \"surname\" varchar, \"age\" integer, \"gender\" integer);")
    data = cursor.fetchall()
    print(data)

if __name__ == "__main__":
    explainFunctionThree()