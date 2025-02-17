import psycopg2


conn = psycopg2.connect(
    "postgresql://db_kaktuskumpels_user:5t9mfzYCYeHURTvDqLaNiybxLul10OcI@dpg-cunh16i3esus73chr9j0-a.oregon-postgres.render.com/db_kaktuskumpels")


def customer_exists(email):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_email = %s", (email,))
    result = cursor.fetchone()

    cursor.close()

    if result is not None:
        return True
    else:
        return False


def insert_customer(vorname, nachname, email, password):
    if customer_exists(email):
        return False

    cursor = conn.cursor()

    insert_statement = """insert into customer (customer_firstname, customer_lastname, customer_email, customer_password)
    values (%s, %s, %s, %s)"""

    cursor.execute(insert_statement, (vorname, nachname, email, password))
    conn.commit()

    count = cursor.rowcount
    print(count, "Record inserted successfully into publisher table")


    cursor.close()

    return True


if __name__ == '__main__':
    cursor = conn.cursor()
    postgreSQL_select_Query = "select * from customer"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from publisher table using cursor.fetchall")
    publisher_records = cursor.fetchall()
    print(publisher_records)

    cursor.close()
    conn.close()
