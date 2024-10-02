import json
from datetime import datetime
from datetime import timezone
import sqlite3
import urllib.request
import sys

con = sqlite3.connect("db.sqlite")

#ICM
#Temperature
#Hourly data for 5 days
url = "https://api.meteo.pl/api/v1/model/wrf/grid/d02_XLONG_XLAT/coordinates/332,266/field/T2/level/0/date/2024-09-30T00/forecast/"
headers = {"Authorization": "Token %s" % sys.argv[1]}
req = urllib.request.Request(url, headers=headers, method="POST")
try:
    with urllib.request.urlopen(req) as f:
        data = json.load(f)
        forecast_date = "2024-09-30T00"
        load_date = datetime.now().isoformat()
        for t, v in zip(data["times"], data["data"]):
            v = v - 273.15  #kelvin to celcius
            con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (t, "temperature", v, "hour", forecast_date, load_date, "ICM"))
        con.commit()
except urllib.error.HTTPError as e:
    print(e, e.read())

#Precipitation
url = "https://api.meteo.pl/api/v1/model/wrf/grid/d02_XLONG_XLAT/coordinates/332%2C266/field/RAINNC/level/0/date/2024-09-30T00/forecast/"
headers = {"Authorization": "Token %s" % sys.argv[1]}
req = urllib.request.Request(url, headers=headers, method="POST")
with urllib.request.urlopen(req) as f:
    data = json.load(f)
    forecast_date = "2024-09-30T00"
    load_date = datetime.now().isoformat()
    for t, v in zip(data["times"], data["data"]):
        con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (t, "precipitation", v, "hour", forecast_date, load_date, "ICM"))
    con.commit()

#AccuWeather - Interia
#Load forecast for 12h
url = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/274663?apikey=%s&metric=true" % sys.argv[2] #code for Warsaw
with urllib.request.urlopen(url) as f:
    data = json.load(f)
    forecast_date = datetime.now().isoformat()
    load_date = datetime.now().isoformat()
    for row in data:
        #print(row)
        #Temperature
        date_value = row["DateTime"]
        value = row["Temperature"]["Value"]
        con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (date_value, "temperature", value, "hour", forecast_date, load_date, "AccuWeather"))
        #PrecipitationProbability
        value = row["PrecipitationProbability"]
        con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (date_value, "precipitation_probability", value, "hour", forecast_date, load_date, "AccuWeather"))
    con.commit()

#Load forecast for 5 days
#Min and max temperature
url = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/274663?apikey=%s&metric=true" % sys.argv[2] #code for Warsaw
with urllib.request.urlopen(url) as f:
    data = json.load(f)
    forecast_date = datetime.now().isoformat()
    load_date = datetime.now().isoformat()
    for row in data["DailyForecasts"]:
        print(row)
   
        date_value = row['Date']
        value_min = row['Temperature']['Minimum']['Value']
        con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (date_value, "temperature min", value_min, "daily", forecast_date, load_date, "AccuWeather"))
    for row in data["DailyForecasts"]:
        date_value = row['Date']
        value_max = row['Temperature']['Maximum']['Value']
        con.execute("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, load_date, source) VALUES(?, ?, ?, ?, ?, ?, ?)", (date_value, "temperature max", value_max, "daily", forecast_date, load_date, "AccuWeather"))
    con.commit()