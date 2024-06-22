import uuid, json, flask, time, sys
from flask import Flask, request
from monster import render, init

app=Flask(__name__)
init(app)

def auth(cookies):
    pass

@app.get("/")
def home():
    header = render("components/header.html", locals())
    footer = render("components/footer.html", locals())
    confetti = render("components/confetti.html", locals())
    return render("components/index.html", locals())

@app.get("/auth")
def login():
    header = render("components/header.html", locals())
    return render("components/login.html", locals())

@app.get("/otp")
def otp():
    header = render("components/header.html", locals())
    return render("components/otp.html", locals())


app.run(host="0.0.0.0", port=int(sys.argv[1]))