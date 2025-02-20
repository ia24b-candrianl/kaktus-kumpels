import os
import shutil
from dbm import error
from time import strftime

import psycopg2

from kaktuskumpels import insert_customer, log_in, get_name_by_email, insert_order_credit, insert_order_rechnung, \
    insert_warenkorb, insert_warenkorb_produkt
from flask import Flask, request, render_template, url_for, redirect, session
from flask_session import Session

# Mock-Daten für die Programmiersprachen
languages = [
    {"name": "Python", "creator": "Guido van Rossum", "year": 1991},
    {"name": "JavaScript", "creator": "Brendan Eich", "year": 1995},
    {"name": "Java", "creator": "James Gosling", "year": 1995},
    {"name": "C#", "creator": "Microsoft", "year": 2000},
    {"name": "Ruby", "creator": "Yukihiro Matsumoto", "year": 1995},
    {"name": "PowerShell", "creator": "Microsoft", "year": 1995},
]

app = Flask(__name__)

session_folder = app.config.get("SESSION_FILE_DIR", "flask_session")
if os.path.exists(session_folder):
    shutil.rmtree(session_folder)
    os.makedirs(session_folder)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.secret_key = "test_key"
Session(app)
from datetime import datetime, timedelta

release_date = datetime(2025, 3, 18, 14, 2, 0)


@app.route("/")
def home() -> str:
    now = datetime.now()
    time_remaining = release_date - now

    days = time_remaining.days
    hours = time_remaining.seconds // 3600
    minutes = (time_remaining.seconds % 3600) // 60
    seconds = time_remaining.seconds % 60
    # app.logger.info("Rendering home page")

    if "benutzername" in session:
        return render_template('home.html', logged_in=True, days=days, hours=hours, minutes=minutes, seconds=seconds)
    else:
        return render_template('home.html', logged_in=False, days=days, hours=hours, minutes=minutes, seconds=seconds)


@app.route("/countdown")
def countdown():
    now = datetime.now()
    diff = release_date - now
    days, seconds = diff.days, diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return render_template("countdown.html", days=days, hours=hours, minutes=minutes, seconds=seconds)


@app.route("/about_flask")
def about_flask() -> str:
    app.logger.info("Rendering About Flask page")
    return render_template("about_flask.html")


@app.route("/contact")
def contact() -> str:
    app.logger.info("Rendering Contact page")
    return render_template("contact.html")


# Route für das Kontaktformular
@app.route("/submit", methods=["POST"])
def submit():
    app.logger.info("Form submitted")
    name = request.form.get("name", "").strip()
    if not name:
        return redirect(url_for("contact"))
    return redirect(url_for("product", name=name))


@app.route("/product")
def product() -> str:
    return render_template("product.html")


@app.route('/ueber_uns')
def ueber_uns():
    return render_template('ueber_uns.html')


@app.route('/registrierung', methods=["GET", "POST"])
def registrierung():
    if 'benutzername' in session:
        return redirect(url_for('success'))

    if request.method == 'POST':
        vorname = request.form.get('vorname')
        nachname = request.form.get('nachname')
        email = request.form.get('email')
        password = request.form.get('password')

        session['vorname'] = vorname
        session['nachname'] = nachname
        session['email'] = email
        session['password'] = password

        if insert_customer(vorname, nachname, email, password):  # Wenn customer_exist True ist.
            return redirect(url_for('success'))
        else:
            return render_template('registrierung.html', error="Diese Anmeldedaten werden bereits verwendet")

    return render_template('registrierung.html')


@app.route('/success')
def success():
    email = session.get('email')
    password = session.get('password')

    if email:
        vorname, nachname = get_name_by_email(email)
    else:
        vorname = session.get('vorname')
        nachname = session.get('nachname')

    return render_template('success.html', email=email, password=password, vorname=vorname, nachname=nachname)


@app.route('/registrierung_vorhanden')
def registrierung_vorhanden():
    return render_template('registrierung_vorhanden.html')


@app.route('/anmelden', methods=['GET', 'POST'])
def anmelden():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        session['email'] = email
        session['password'] = password

        user = log_in(email, password)

        if user:
            session['benutzername'] = user[1]
            session['email'] = user[3]
            return redirect(url_for('success'))
        else:
            return render_template('anmelden.html', error="Das Passwort oder der Benutzername ist Falsch.")

    return render_template('anmelden.html', log_in=False)


@app.route('/warenkorb_leer')
def warenkorb_leer():
    return render_template('warenkorb_leer.html')


@app.route('/profilübersicht')
def profilübersicht():
    bestellungen = session.get('bestellungen', [])
    return render_template('profilübersicht.html', bestellungen=bestellungen)


@app.route('/profilübersicht_leer')
def profilübersicht_leer():
    return render_template('profilübersicht_leer.html')


@app.route('/warenkorb')
def warenkorb():
    bestellungen = session.get('bestellungen', [])

    return render_template('warenkorb.html', bestellungen=bestellungen)


@app.route('/warenkorb_bezahlen', methods=["GET", "POST"])
def warenkorb_bezahlen():
    bestellungen = session.get('bestellungen', [])
    if request.method == 'POST':
        amount = int(request.form.get('amount'))
        email = session.get('email')

        if amount <= 0:
            return render_template('warenkorb_bezahlen.html', error="Wählen sie eine gültige Anzahl aus!")
        elif email:
            erfolg = insert_warenkorb(amount, email)
            if erfolg:
                insert_warenkorb_produkt(amount, email)
                return redirect(url_for('bezahlseite'))
        else:
            return render_template('warenkorb_bezahlen.html', error="Kein Benutzer eingeloggt")

    return render_template('warenkorb_bezahlen.html', bestellungen=bestellungen)


@app.route('/bezahlseite', methods=["GET", "POST"])
def bezahlseite():
    if request.method == 'POST':
        kartennummer = request.form.get('kartennummer')
        sicherheitscode = request.form.get('sicherheitscode')
        vorname = request.form.get('vorname')
        nachname = request.form.get('nachname')
        ablaufdatum = request.form.get('ablaufdatum')
        email = request.form.get('email')

        session['kartennummer'] = kartennummer
        session['sicherheitscode'] = sicherheitscode
        session['vorname'] = vorname
        session['nachname'] = nachname
        session['ablaufdatum'] = ablaufdatum
        session['email'] = email

        if 'bestellungen' not in session:
            session['bestellungen'] = []

        bestellungen = session.get('bestellungen', [])

        bestellungen.append({
            'Produkt': "Arctic Air 2.0",
            'Bestelldatum': datetime.now().strftime('%d.%m.%Y %H:%M'),
            'Bezahlstatus': "bezahlt",
            'Preis': "1008.90 CHF",
            'Bezahlart': "Kartenzahlung",
            'Versandstatus': "Versendet"
        })

        session['bestellungen'] = bestellungen
        session.modified = True

        if insert_order_credit(kartennummer, sicherheitscode, vorname, nachname, ablaufdatum, email):
            return redirect(url_for('bestellbestätigung'))
        else:
            return render_template('bezahlseite.html', error="Sie verfügen noch über keinen Account")

    return render_template('bezahlseite.html')


@app.route('/bezahlseite1', methods=["GET", "POST"])
def bezahlseite1():
    if request.method == 'POST':
        adresse = request.form.get('adresse')
        nachname = request.form.get('nachname')
        vorname = request.form.get('vorname')
        email = request.form.get('email')

        session['adresse'] = adresse
        session['nachname'] = nachname
        session['vorname'] = vorname
        session['email'] = email

        if 'bestellungen' not in session:
            session['bestellungen'] = []

        session['bestellungen'].append({
            'Produkt': "Arctic Air 2.0",
            'Bestelldatum': datetime.now().strftime('%d.%m.%Y %H:%M'),
            'Bezahlstatus': "bezahlt",
            'Preis': "1008.90 CHF",
            'Bezahlart': "Rechnung",
            'Versandstatus': "In Bearbeitung"
        })

        session.modified = True

        if insert_order_rechnung(adresse, nachname, vorname, email):
            return redirect(url_for('bestellbestätigung_rechnung'))
        else:
            return render_template('bezahlseite.html', error="Sie verfügen über noch keinen Account")

    return render_template('bezahlseite.html')


@app.route('/bestellbestätigung')
def bestellbestätigung():
    kartennummer = session.get('kartennummer')
    sicherheitscode = session.get('sicherheitscode')
    vorname = session.get('vorname')
    nachname = session.get('nachname')
    ablaufdatum = session.get('ablaufdatum')
    email = session.get('email')

    return render_template('bestellbestätigung.html', kartennummer=kartennummer, sicherheitscode=sicherheitscode,
                           vorname=vorname, nachname=nachname, ablaufdatum=ablaufdatum, email=email, products=product)


@app.route('/bestellbestätigung_rechnung')
def bestellbestätigung_rechnung():
    adresse = session.get('adresse')
    nachname = session.get('nachname')
    vorname = session.get('vorname')
    email = session.get('email')

    return render_template('bestellbestätigung_rechnung.html', adresse=adresse, nachname=nachname, vorname=vorname,
                           email=email, products=product)




# API für Programmiersprachen als JSON
from flask import jsonify

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/helloWorld')
def hello_world() -> str:
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
