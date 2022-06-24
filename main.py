from waitress import serve
from flask import Flask, render_template, send_from_directory
import os
from database import DatabaseManager
import json

db = DatabaseManager()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit")
def submit():
    return render_template("submit.html", categories=db.basic_category_list())


@app.route("/list.json")
def get_list():
    return db.tip_list_to_json_cached()


@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("assets/", path)


HOST = "0.0.0.0"
PORT = 8072
print(f"Starting on {HOST}:{PORT}")
if os.name == "nt":
    app.run(HOST, PORT, debug=True)
else:
    serve(app, host=HOST, port=PORT)
