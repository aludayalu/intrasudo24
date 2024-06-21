import uuid, json, flask, time, sys
from flask import Flask, request
from monster import render, init

app=Flask(__name__)
init(app)

@app.get("/")
def home():
    header = render("components/header.html", locals())
    footer = render("components/footer.html", locals())
    return render("components/index.html", locals())


app.run(host="0.0.0.0", port=int(sys.argv[1]))