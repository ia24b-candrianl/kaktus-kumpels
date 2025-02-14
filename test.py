from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/math')
def math():
    return str(2 + 2)

@app.route("/parameter/<name>")
def result(name) -> str:
    return name

if __name__ == '__main__':
    app.run(debug=True)