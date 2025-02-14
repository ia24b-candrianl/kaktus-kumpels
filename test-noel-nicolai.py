import psycopg2

conn = psycopg2.connect(
    "postgresql://test_noel_nicolai_user:JbgbjDupKpm79sQDnVclCzgLk2666q57@dpg-cumso5l6l47c73989jr0-a.oregon-postgres.render.com/test_noel_nicolai")


def insert(cursor):
    insert_statement = """insert into customer (customer_id, customer_firstname, customer_lastname, customer_password)
    values (%s, %s, %s, %s)"""

    insertion = [(1, 'Nicolai', 'Halbheer', '123456'),
                 (2, 'Noel', 'Hug', '123456'),]

    for insert in insertion:
        cursor.execute(insert_statement, insert)
        count = cursor.rowcount
        print(count, "Record inserted successfully into publisher table")


if __name__ == '__main__':
    cursor = conn.cursor()
    insert(cursor)
    postgreSQL_select_Query = "select * from customer"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from publisher table using cursor.fetchall")
    publisher_records = cursor.fetchall()
    print(publisher_records)

    cursor.close()
    conn.close()
