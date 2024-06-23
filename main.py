import uuid, json, flask, time, sys
from flask import Flask, request, redirect
from monster import render, init
from database import get, set, get_All
from mailer import mail
import re, hashlib, random
from secrets_parser import parse

salt = parse("variables.txt")["salt"]

admin=["r23025aarav@dpsrkp.net"]
profanity=open("profanity.txt").read()

app = Flask(__name__)
init(app)


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?@dpsrkp\.net$"
    return re.match(pattern, email) is not None


def User():
    return {
        "name": "",
        "level": 0,
        "logs": "",
        "email": "",
        "verified": False,
        "password": "",
    }


def auth(cookies):
    if "email" in cookies:
        account = get("accounts", cookies["email"])
        if account["Ok"] == False:
            return account
        if (
            account["Value"]["password"]
            == hashlib.sha256(cookies["password"].encode()).hexdigest()
        ):
            return account
        else:
            return {"Ok": False}
    else:
        return {"Ok": False}


@app.get("/")
def home():
    loggedIn = auth(dict(request.cookies))
    if loggedIn["Ok"]:
        status = "Logout"
        status_url = "/logout"
    else:
        status = "Log In"
        status_url = "/auth"
    header = render("components/header.html", locals())
    footer = render("components/footer.html", locals())
    confetti = render("components/confetti.html", locals())
    if loggedIn["Ok"]:
        countdown = render("countdown", locals())
    else:
        countdown = render("signinbutton", locals())
    return render("components/index.html", locals())


@app.get("/leaderboard")
def leaderboard():
    loggedIn = auth(dict(request.cookies))
    logs_text = ""
    if loggedIn["Ok"]:
        if request.cookies.get("email") in admin:
            logs_text = "Logs"
    fetchedData = get_All("leaderboard")
    levels={}
    for x in fetchedData["Value"]:
        if x["level"] not in levels:
            levels[x["level"]]=[x]
        else:
            levels[x["level"]].append({"time":x["time"], "name":x["name"], "email":x["email"], "level":x["level"]})
    leaderboard_data=[]
    players_added=[]
    for level in sorted(levels)[::-1]:
        level=levels[level]
        level.sort(key=lambda data: data["time"])
        for player in level:
            if player["email"] not in players_added:
                leaderboard_data.append({"time":player["time"], "name":player["name"], "level":player["level"]})
                players_added.append(player["email"])

    leaderboard = []

    for i in range(len(leaderboard_data)):
        name = leaderboard_data[i]["name"]
        level = leaderboard_data[i]["level"]
        logs = []
        if request.cookies.get("email") in admin and False:
            for log in leaderboard_data[i]["logs"]:
                logs.append(render("components/leaderboard/modal.html", locals()))

        rank = i + 1

        leaderboard.append(render("components/leaderboard/card.html", locals()))

    if loggedIn["Ok"]:
        status = "Logout"
        status_url = "/logout"
    else:
        status = "Log In"
        status_url = "/auth"
    header = render("components/header.html", locals())
    footer = render("components/footer.html", locals())
    return render("components/leaderboard/leaderboard.html", locals())


@app.get("/logout")
def logout():
    return render("logout", locals())


@app.get("/auth")
def auth_page():
    loggedIn = auth(dict(request.cookies))
    if loggedIn["Ok"]:
        status = "Logout"
        status_url = "/logout"
    else:
        status = "Log In"
        status_url = "/auth"
    header = render("components/header.html", locals())
    return render("components/auth.html", locals())


@app.get("/api/auth")
def auth_api():
    args = dict(request.args)
    if "password" not in args or "email" not in args or "method" not in args:
        return json.dumps({"error": "Missing Fields", "args": args})
    if is_valid_email(args["email"]):
        if get("emails", args["email"])["Ok"]:
            account = get("accounts", args["email"])["Value"]
            if (
                account["password"]
                == hashlib.sha256(args["password"].encode()).hexdigest()
            ):
                return json.dumps({"success": True})
            else:
                return json.dumps({"error": "Incorrect Password"})
        else:
            if "name" not in args or "otp" not in args:
                return json.dumps({"error": "Missing Fields", "args": args})
            args["name"].replace("\t", "").replace("  ", " ")
            if len(args["name"].split(" "))>2:
                return json.dumps({"error":"Name can only contain first name and last name"})
            for x in args["name"].replace(" ", ""):
                if x not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    return json.dumps({"error":"Name can only contain alphabets"})
            if args["name"].count(" ")>2:
                return json.dumps("Name can only contain a first name and a last name")
            for x in args["name"].split(" "):
                if x in profanity:
                    return json.dumps({"error":"Profanity Detected"})
            if args["otp"] == get_otp(args["email"]):
                set("emails", args["email"], {"email":args["email"], "time":time.time()})
                user = User()
                user["email"] = args["email"]
                user["name"] = args["name"].title()
                user["password"] = hashlib.sha256(args["password"].encode()).hexdigest()
                set("accounts", args["email"], user)
                set("leaderboard", args["email"]+"_0", {"email":args["email"] ,"time":time.time(), "level":0, "name":args["name"]})
                return json.dumps({"success": True})
            else:
                if args["method"]=="login":
                    return json.dumps({"error":"Account does not exist"})
                else:
                    return json.dumps({"error": "Wrong OTP"})
    return json.dumps({"error": "Invalid Email"})


def get_otp(email):
    digest = hashlib.sha256((email+salt).encode()).digest()
    random.seed(int.from_bytes(digest, "big"))
    otp = str(random.randint(0, 999999))
    return "0" * (6 - len(otp)) + otp


@app.get("/send_otp")
def sendotp():
    args = dict(request.args)
    if "email" not in args:
        return json.dumps({"error": "Missing Fields"})
    if is_valid_email(args["email"]):
        otp=get_otp(args["email"])
        digit1=otp[0]
        digit2=otp[1]
        digit3=otp[2]
        digit4=otp[3]
        digit5=otp[4]
        digit6=otp[5]
        mail(
            args["email"],
            "Intra Sudo 2024 OTP Verification",
            render("mail/otp", locals()),
        )
        return json.dumps({"otp": "success"})
    else:
        return json.dumps({"error": "Invalid Email"})

@app.get("/admin")
def admin_page():
    loggedIn = auth(dict(request.cookies))
    if request.cookies.get("email") in admin:
        return render("admin")
    return ""

app.run(host="0.0.0.0", port=int(sys.argv[1]))
