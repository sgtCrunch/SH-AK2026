from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def front_page():
    return render_template("index.html")


@app.route("/baby-clue")
def baby_clue():
    return render_template("baby-clue.html")