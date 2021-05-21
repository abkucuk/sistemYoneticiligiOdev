from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import date, datetime

import os
import socket

app = Flask(__name__)

client = MongoClient("mongo:27017")
my_db = client["sistemYon"]
my_col = my_db["visitors"]


@app.route('/')
def home():
    ip = request.headers['X-Real-IP']
    today = (date.today()).strftime("%d/%m/%Y")
    time = (datetime.now()).strftime("%H:%M:%S")

    print(ip)

    data = {
        "ip": ip,
        "day": today,
        "time": time
    }

    my_col.insert_one(data)

    findings = my_col.find({}, {"_id": 0, "ip": 1, "day": 1, "time": 1})

    results = []

    for i in findings:
        results.append(i)

    return render_template('home.html', cli_ip=ip, visitors=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)