from flask import Flask, request, render_template, url_for, redirect
import services.math_service as math_service

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

@app.route("/")
def home() -> str:
    print(math_service.add(1.0, 2.0))
    app.logger.info("Rendering home page")
    return render_template("home.html")

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
    return redirect(url_for("result", name=name))

@app.route("/product")
def result() -> str:
    return render_template("product.html")

@app.route('/ueber_uns')
def ueber_uns():
    return render_template('ueber_uns.html')

@app.route('/registrierung')
def registrierung():
    return render_template('registrierung.html')


# API für Programmiersprachen als JSON
from flask import jsonify
@app.route("/api/languages")
def api_languages():
    return jsonify(languages)

@app.route('/helloWorld')
def hello_world() -> str:
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

