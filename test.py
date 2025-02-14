import psycopg2

conn = psycopg2.connect(
    "postgresql://demo_flask_user:RjfyvdnXWY6JETLAseziwFESB7obYYR1@dpg-cumrp0d2ng1s739pj3u0-a.oregon-postgres.render.com/demo_flask"
)


def insert(cursor):
    insert_statement = """insert into person (person_id, first_name, last_name, birth_date)
    values (%s, %s, %s, %s)"""
    record_to_insert = [(3, 'Bruce', 'Bennet', '1950-08-01'),
                        (4, 'Ms', 'Marvel', '1920-01-01')
                        ]
    for record in record_to_insert:
        cursor.execute(insert_statement, record)
        count = cursor.rowcount
        print(count, "Record inserted successfully into publisher table")

if __name__ == '__main__':
    cursor = conn.cursor()
    insert(cursor)
    postgreSQL_select_Query = "select * from person"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from publisher table using cursor.fetchall")
    publisher_records = cursor.fetchall()
    print(publisher_records)

    cursor.close()
    conn.close()
