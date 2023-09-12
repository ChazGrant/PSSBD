import psycopg2


CONFIG = {
            "database": "ambulance",
            "user": "ambulance_admin",
            "password": "secretpassword",
            "host": "127.0.0.1",
            "port": 5432
        }

conn = psycopg2.connect(**CONFIG)
cursor = conn.cursor()

cursor.execute("Select * FROM sick_people LIMIT 0")
colnames = [desc[0] for desc in cursor.description]
print(colnames)
