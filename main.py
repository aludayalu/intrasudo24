import uuid, json, flask, time, sys
from flask import Flask, request
from render import render

app=Flask(__name__)

@app.get("/")
def home():
    name="aludayalu"
    return render("components/index.html", locals())

app.run(host="0.0.0.0", port=int(sys.argv[1]))