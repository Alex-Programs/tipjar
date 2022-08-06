from waitress import serve
from flask import Flask, render_template, send_from_directory, request, redirect
import os
from database import DatabaseManager
import json
import base64
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = DatabaseManager()

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["9000 per day"]
)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")

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


@limiter.limit("10 per minute")
@limiter.limit("30 per day")
@app.route("/submit_new", methods=["POST"])
def submit_new():
    data = json.loads(request.data)
    print(data)

    if db.messageid_exists(data["messageid"]):
        return "Message already exists", 409

    if len(data["messagetext"]) > 300:
        return "Message text too long", 400

    flag_messages = {
        "dw11o;<vy": {"text": "Error 500, Internal Server Error.", "code": 500},
        "0967r": {"text": "Error 500 waitress exception", "code": 502}
        # Faking messages
    }

    decoded = base64.b64decode(data["token"]).decode("utf-8")

    if flag_messages.get(decoded.split("@@")[-1]):
        with open("logs.txt", "a") as f:
            f.write(
                str(request.headers.get("CF-Connecting-IP")) + "::" + data["token"] + "::" + data["messageid"] + "::" +
                data["category"] + "::" + data[
                    "messagetext"] + "\n WAS FLAGGED AND FAKED ERROR \n\n\n\n\n\n\n\n ---------- \n\n\n\n\n\n\n\n")

        return flag_messages[decoded.split("@@")[-1]]["text"], flag_messages[decoded.split("@@")[-1]]["code"]

    result = db.add_new_tip(data["messageid"].strip(), data["messagetext"].strip(), data["category"], data.get("fulllink"))

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
