import json
from datetime import datetime
from datetime import timezone
import sqlite3
import urllib.request
import sys

con = sqlite3.connect("db.sqlite")

#ICM
url = "https://api.meteo.pl/api/v1/model/coamps/grid/2a/coordinates/130,111/field/airtmp_zht_fcstfld/level/000002_000000/date/2017-11-11T00/forecast/"
headers = {"Authorization": "Token %s" % sys.argv[1]}
req = urllib.request.Request(url, headers=headers, method="POST")
with urllib.request.urlopen(req) as f:
    data = json.load(f)
    forecast_date = "2017-11-11T00"
    load_date = datetime.now().isoformat()
    for t, v in zip(data["times"], data["data"]):
        v = v - 273.15  #kelvin to celcius
        con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (t, "temperature", v, "hour", forecast_date, load_date, "ICM"))
        #print(t, v)
    con.commit()

#AccuWeather
#Load forecast for 12h
url = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/274663?apikey=%s&metric=true" % sys.argv[2] #code for Warsaw
with urllib.request.urlopen(url) as f:
    data = json.load(f)
    forecast_date = datetime.now().isoformat()
    load_date = datetime.now().isoformat()
    for row in data:
        date_value = row["DateTime"]
        value = row["Temperature"]["Value"]
        #print(date_value, value)
        con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (date_value, "temperature", value, "hour", forecast_date, load_date, "AccuWeather"))
    con.commit()

#Load forecast for 5 days
#Min and max temperature
url = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/274663?apikey=%s&metric=true" % sys.argv[2] #code for Warsaw
with urllib.request.urlopen(url) as f:
    data = json.load(f)
    forecast_date = datetime.now().isoformat()
    load_date = datetime.now().isoformat()
    for row in data["DailyForecasts"]:
        date_value = row['Date']
        value_min = row['Temperature']['Minimum']['Value']
        con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (date_value, "temperature min", value_min, "daily", forecast_date, load_date, "AccuWeather"))
    for row in data["DailyForecasts"]:
        date_value = row['Date']
        value_max = row['Temperature']['Maximum']['Value']
        con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (date_value, "temperature max", value_max, "daily", forecast_date, load_date, "AccuWeather"))
    con.commit()