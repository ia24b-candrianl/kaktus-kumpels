import psycopg2

conn = psycopg2.connect("postgresql://db_kaktuskumpels_user:5t9mfzYCYeHURTvDqLaNiybxLul10OcI@dpg-cunh16i3esus73chr9j0-a.oregon-postgres.render.com/db_kaktuskumpels")

def insert_customer(cursor):
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
    #insert_customer(cursor)
    postgreSQL_select_Query = "select * from customer"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from publisher table using cursor.fetchall")
    publisher_records = cursor.fetchall()
    print(publisher_records)

    cursor.close()
    conn.close()