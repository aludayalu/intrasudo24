import uuid, json, flask, time, sys
from flask import Flask, request
from monster import render, init
from database import get, set
from mailer import mail

app=Flask(__name__)
init(app)

def User():
    return {"id":0, "name":"", "level":0, "logs":"", "email":"", "verified":False, "password":""}

def auth(cookies):
    if "loggedIn" in cookies:
        return get("tokens", cookies["loggedIn"])
    else:
        return {"Ok":False}

@app.get("/")
def home():
    loggedIn=auth(dict(request.cookies))
    header = render("components/header.html", locals())
    footer = render("components/footer.html", locals())
    confetti = render("components/confetti.html", locals())
    return render("components/index.html", locals())


app.run(host="0.0.0.0", port=int(sys.argv[1]))