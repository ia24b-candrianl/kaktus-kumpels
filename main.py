from flask import Flask, request, render_template, url_for, redirect, session

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
app.secret_key = "test_key"
from datetime import datetime

release_date = datetime(2025, 3, 18, 14, 2, 0)


@app.route("/")
def home() -> str:
    now = datetime.now()
    time_remaining = release_date - now

    days = time_remaining.days
    hours = time_remaining.seconds // 3600
    minutes = (time_remaining.seconds % 3600) // 60
    seconds = time_remaining.seconds % 60
    app.logger.info("Rendering home page")
    return render_template("home.html", days=days, hours=hours, minutes=minutes, seconds=seconds)


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
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        return redirect(url_for('success'))

    return render_template('registrierung.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/warenkorb_leer')
def warenkorb_leer():
    return render_template('warenkorb_leer.html')


@app.route('/profilübersicht')
def profilübersicht():
    return render_template('profilübersicht.html')


@app.route('/warenkorb')
def warenkorb():
    return render_template('warenkorb.html')


@app.route('/bezahlseite', methods=["GET", "POST"])
def bezahlseite():
    if request.method == 'POST':
        kartennummer = request.form.get('kartennummer')
        sicherheitscode = request.form.get('sicherheitscode')
        name = request.form.get('name')
        ablaufdatum = request.form.get('ablaufdatum')

        session['kartennummer'] = kartennummer
        session['sicherheitscode'] = sicherheitscode
        session['name'] = name
        session['ablaufdatum'] = ablaufdatum

        return redirect(url_for('bestellbestätigung'))

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

        return redirect(url_for('bestellbestätigung_rechnung'))

    return render_template('bezahlseite.html')


@app.route('/bestellbestätigung')
def bestellbestätigung():
    kartennummer = session.get('kartennummer')
    sicherheitscode = session.get('sicherheitscode')
    name = session.get('name')
    ablaufdatum = session.get('ablaufdatum')

    return render_template('bestellbestätigung.html',
                           kartennummer=kartennummer,
                           sicherheitscode=sicherheitscode,
                           name=name,
                           ablaufdatum=ablaufdatum)


@app.route('/bestellbestätigung_rechnung')
def bestellbestätigung_rechnung():
    adresse = session.get('adresse')
    nachname = session.get('nachname')
    vorname = session.get('vorname')
    email = session.get('email')

    return render_template('bestellbestätigung_rechnung.html', adresse=adresse, nachname=nachname, vorname=vorname,
                           email=email)


# API für Programmiersprachen als JSON
from flask import jsonify


@app.route('/helloWorld')
def hello_world() -> str:
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
