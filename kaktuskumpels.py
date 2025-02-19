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


def log_in(email, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_email = %s AND customer_password = %s", (email, password))
    result = cursor.fetchone()
    cursor.close()

    if result is not None:
        return result
    else:
        return None


def get_name_by_email(email):
    cursor = conn.cursor()
    cursor.execute("SELECT customer_firstname, customer_lastname FROM customer WHERE customer_email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result[0], result[1]
    return None, None


def insert_order_credit(kartennummer, sicherheitscode, vorname, nachname, ablaufdatum, customer_email):
    cursor = conn.cursor()

    cursor.execute("SELECT customer_id FROM customer WHERE customer_email = %s", (customer_email,))
    customer_id_result = cursor.fetchone()

    if customer_id_result is None:
        print(f"Error: Registriere dich zuerst {customer_email}")
        cursor.close()
        return False
    else:

        customer_id = customer_id_result[0]

        insert_statement = """insert into bestellung_credit (customer_id, card_number, safety_code, first_name, last_name, expiration)
            values (%s, %s, %s, %s, %s, %s)"""

        cursor.execute(insert_statement, (customer_id, kartennummer, sicherheitscode, vorname, nachname, ablaufdatum))
        conn.commit()

        count = cursor.rowcount
        print(count, "Record inserted successfully into bestellung_credit table")

        cursor.close()

        return True


def insert_order_rechnung(adresse, nachname, vorname, email):
    cursor = conn.cursor()

    cursor.execute("SELECT customer_id FROM customer WHERE customer_email = %s", (email,))
    customer_id_result = cursor.fetchone()

    if customer_id_result is None:
        print(f"Error: Registriere dich zuerst {email}")
        cursor.close()
        return False
    else:

        customer_id = customer_id_result[0]

        insert_statement = """insert into bestellung_rechnung (customer_id, adress, last_name, first_name, email)
                    values (%s, %s, %s, %s, %s)"""

        cursor.execute(insert_statement, (customer_id, adresse, nachname, vorname, email))
        conn.commit()

        count = cursor.rowcount
        print(count, "Record inserted successfully into bestellung_credit table")

        cursor.close()

        return True


def insert_warenkorb(amount, customer_email):
    cursor = conn.cursor()

    cursor.execute("SELECT customer_id from customer where customer_email = %s", (customer_email, ))
    customer_id_result = cursor.fetchone()

    if customer_id_result is None:
        print("Keinen Benutzer gefunden")
        cursor.close()
        return False

    else:
        customer_id = customer_id_result[0]

        insert_statement = """insert into warenkorb (customer_id, amount )
                    values (%s, %s)"""

        cursor.execute(insert_statement, (customer_id, amount))
        conn.commit()

        count = cursor.rowcount
        print(count, "Record inserted successfully into warenkorb")

        cursor.close()

        return True


if __name__ == '__main__':
    cursor = conn.cursor()

    postgreSQL_select_Query_customer = "SELECT * FROM customer"
    cursor.execute(postgreSQL_select_Query_customer)
    customer_records = cursor.fetchall()
    print("\nAlle registrierte Kunden:")
    print(customer_records)

    postgreSQL_select_Query_order_credit = "SELECT * FROM bestellung_credit"
    cursor.execute(postgreSQL_select_Query_order_credit)
    bestellung_credit_records = cursor.fetchall()
    print("\nGetätigte Bestellungen per Karte:")
    print(bestellung_credit_records)

    postgreSQL_select_Query_order_rechnung = "SELECT * FROM bestellung_rechnung"
    cursor.execute(postgreSQL_select_Query_order_rechnung)
    order_credit_records = cursor.fetchall()
    print("\nGetätigte Bestellungen per Rechnung:")
    print(order_credit_records)

    postgreSQL_select_Query_warenkorb = "SELECT * FROM warenkorb"
    cursor.execute(postgreSQL_select_Query_warenkorb)
    warenkorb_records = cursor.fetchall()
    print("\nIm Warenkorb vorhanden:")
    print(warenkorb_records)

    cursor.close()
    conn.close()
