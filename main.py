import uuid, json, flask, time, sys
from flask import Flask, request, redirect
from monster import render, init
from database import get, set
from mailer import mail
import re, hashlib, random
from secrets_parser import parse

salt = parse("variables.txt")["salt"]

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
    fetchedData = [
        {"name": "AyonC", "level": 1, "logs": ["adsf", "dosometing"]},
        {"name": "Alu", "level": 10, "logs": []},
    ]
    fetchedData.sort(key=lambda data: data["level"], reverse=True)

    leaderboard = []

    for i in range(len(fetchedData)):
        name = fetchedData[i]["name"]
        level = fetchedData[i]["level"]
        points = 1
        logs = []
        for log in fetchedData[i]["logs"]:
            logs.append(render("components/leaderboard/modal.html", locals()))

        rank = i + 1

        leaderboard.append(render("components/leaderboard/card.html", locals()))

    loggedIn = auth(dict(request.cookies))
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


@app.get("/otp")
def otp():
    loggedIn = auth(dict(request.cookies))
    if loggedIn["Ok"]:
        status = "Logout"
        status_url = "/logout"
    else:
        status = "Log In"
        status_url = "/auth"
    header = render("components/header.html", locals())
    return render("components/otp.html", locals())


@app.get("/api/auth")
def auth_api():
    args = dict(request.args)
    if "password" not in args or "email" not in args:
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
            if args["otp"] == get_otp(args["email"]):
                set("emails", args["email"], str(time.time()))
                user = User()
                user["email"] = args["email"]
                user["name"] = args["name"]
                user["password"] = hashlib.sha256(args["password"].encode()).hexdigest()
                set("accounts", args["email"], user)
                return json.dumps({"success": True})
            else:
                return json.dumps({"error": "Wrong OTP"})
    return json.dumps({"error": "Invalid Email"})


def get_otp(email):
    digest = hashlib.sha256(email.encode()).digest()
    random.seed(int.from_bytes(digest, "big"))
    otp = str(random.randint(0, 999999))
    return "0" * (6 - len(otp)) + otp


@app.get("/send_otp")
def sendotp():
    args = dict(request.args)
    if "email" not in args:
        return json.dumps({"error": "Missing Fields"})
    if is_valid_email(args["email"]):
        mail(
            args["email"],
            "Intra Sudo 2024 OTP Verification",
            "Here is your OTP<br>" + get_otp(args["email"]),
        )
        return json.dumps({"otp": "success"})
    else:
        return json.dumps({"error": "Invalid Email"})


app.run(host="0.0.0.0", port=int(sys.argv[1]))
