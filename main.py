from waitress import serve
from flask import Flask, render_template, send_from_directory, request, redirect
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


@app.route("/existing_url")
def check_existing_url():
    mid = request.args.get("messageid")

    if not mid:
        return "Invalid Request", 400

    for category in db.tip_list["categories"]:
        for tip in category["tips"]:
            if str(tip["messageid"].strip()) == str(mid.strip()):
                return "Message ID exists", 409

    return "Doesn't exist", 200


@app.route("/submit_new", methods=["POST"])
def submit_new():
    data = json.loads(request.data)
    print(data)

    if db.messageid_exists(data["messageid"]):
        return "Message already exists", 409

    if len(data["messagetext"]) > 300:
        return "Message text too long", 400

    result = db.add_new_tip(data["messageid"].strip(), data["messagetext"].strip(), data["category"])

    if result == False:
        return "Something went wrong. Is the category valid?", 400

    # wiped at midnight daily by a shell script. IPs (+ other info) only viewed and used for quietly blocking spammers if we get any.
    with open("logs.txt", "a") as f:
        f.write(str(request.headers.get("CF-Connecting-IP")) + "::" + data["token"] + "::" + data["messageid"] + "::" +
                data["category"] + "::" + data["messagetext"] + "\n\n\n\n\n\n\n\n ---------- \n\n\n\n\n\n\n\n")

    return "OK", 200


@app.route("/get_keywords")
def get_keywords():
    categoriesToSend = {}
    for category in db.tip_list["categories"]:
        categoriesToSend[category["name"]] = category["keywords"]

    return json.dumps(categoriesToSend)


@app.route("/admin")
def admin():
    with open("admin_pwd.txt") as f:
        if request.cookies.get("password") != f.readlines()[0].strip():
            return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ", code=302)

    return render_template("admin.html")


@app.route("/admin_delete", methods=["POST"])
def admin_delete():
    with open("admin_pwd.txt") as f:
        if request.cookies.get("password") != f.readlines()[0].strip():
            return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ", code=302)

    uid = json.loads(request.data)["uid"]

    db.remove_by_id(uid)

    return "Done. Maybe."


HOST = "0.0.0.0"
PORT = 8075
print(f"Starting on {HOST}:{PORT}")
if os.name == "nt":
    app.run(HOST, PORT, debug=True)
else:
    serve(app, host=HOST, port=PORT)
