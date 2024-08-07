import json
from datetime import datetime
import sqlite3
import urllib.request
import sys

con = sqlite3.connect("db.sqlite")

url = "https://api.meteo.pl/api/v1/model/coamps/grid/2a/coordinates/130,111/field/airtmp_zht_fcstfld/level/000002_000000/date/2017-11-11T00/forecast/"
headers = {"Authorization": "Token %s" % sys.argv[1]}
req = urllib.request.Request(url, headers=headers, method="POST")
with urllib.request.urlopen(req) as f:
    data = json.load(f)
    forecast_date = "2017-11-11T00"
    now = datetime.now()
    load_date = now.strftime("%d-%m-%Y %H:%M:%S")
    for t, v in zip(data["times"], data["data"]):
        v = v - 273.15  #kelvin to celcius
        con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (t, "temperature", v, "hour", forecast_date, load_date, "ICM"))
    con.commit()
    