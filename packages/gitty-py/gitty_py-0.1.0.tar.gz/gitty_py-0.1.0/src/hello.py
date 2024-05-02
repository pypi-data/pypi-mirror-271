from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/contact")
def contact():
    return "<p>Hello, You are in contact page!</p>"
