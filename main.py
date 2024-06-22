import uuid, json, flask, time, sys
from flask import Flask, request, redirect
from monster import render, init
from database import get, set
from mailer import mail
import re, hashlib

app=Flask(__name__)
init(app)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?@dpsrkp\.net$'
    return re.match(pattern, email) is not None

def User():
    return {"name":"", "level":0, "logs":"", "email":"", "verified":False, "password":""}

def auth(cookies):
    if "email" in cookies:
        return get("emails", cookies["email"])
    else:
        return {"Ok":False}

@app.get("/")
def home():
    loggedIn=auth(dict(request.cookies))
    if loggedIn["Ok"]:
        status="Logout"
        status_url="/logout"
    else:
        status="Log In"
        status_url="/auth"
    header = render("components/header.html", locals())
    footer = render("components/footer.html", locals())
    confetti = render("components/confetti.html", locals())
    if loggedIn["Ok"]:
        countdown=render("countdown", locals())
    else:
        countdown=render("signinbutton", locals())
    return render("components/index.html", locals())

@app.get("/logout")
def logout():
    response=redirect("/")
    response.set_cookie("email", "")
    response.set_cookie("password", "")
    return response

@app.get("/auth")
def auth_page():
    loggedIn=auth(dict(request.cookies))
    if loggedIn["Ok"]:
        status="Logout"
        status_url="/logout"
    else:
        status="Log In"
        status_url="/auth"
    header = render("components/header.html", locals())
    return render("components/auth.html", locals())

@app.get("/otp")
def otp():
    loggedIn=auth(dict(request.cookies))
    if loggedIn["Ok"]:
        status="Logout"
        status_url="/logout"
    else:
        status="Log In"
        status_url="/auth"
    header = render("components/header.html", locals())
    return render("components/otp.html", locals())

@app.get("/api/auth")
def auth_api():
    args=dict(request.args)
    if "password" not in args or "email" not in args or "name" not in args or "otp" not in args:
        return json.dumps({"error":"Missing Fields"})
    if is_valid_email(args["email"]):
        if get("emails", args["email"])["Ok"]:
            account=get("accounts", args["email"])["Value"]
            if account["password"]==hashlib.sha256(args["password"].encode()).hexdigest():
                return json.dumps({"success":True})
            else:
                return json.dumps({"error":"Incorrect Password"})
        else:
            set("emails", args["email"], str(time.time()))
            user=User()
            user["email"]=args["email"]
            user["name"]=args["name"]
            user["password"]=hashlib.sha256(args["password"].encode()).hexdigest()
            set("accounts", args["email"], user)
            return json.dumps({"success":True})
    return json.dumps({"error":"Invalid Email"})


app.run(host="0.0.0.0", port=int(sys.argv[1]))