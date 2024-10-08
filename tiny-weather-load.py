import json
from datetime import datetime, timedelta
from datetime import timezone
import sqlite3
import urllib.request
import sys
import itertools
import tomllib

def fetch_icm(model, grid, coords, field, level, token):
    date = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%dT00")
    url = "https://api.meteo.pl/api/v1/model/%s/grid/%s/coordinates/%s/field/%s/level/%d/date/%s/forecast/" \
        % (model, grid, coords, field, level, date)

    headers = {"Authorization": "Token %s" % token}
    req = urllib.request.Request(url, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as f:
            data = json.load(f)
    except urllib.error.HTTPError as e:
        print(e, e.read())
        raise

    assert field in ("T2", "RAINNC")
    if field == "T2":
        data["data"] = [x-273.15 for x in data["data"]]
        metric = "temperature"
    elif field == "RAINNC":
        metric = "precipitation"
    return [(x, metric, y, "hour", date, "ICM") for x, y in zip(data["times"], data["data"])]

def fetch_aw(forecast, period, loc_key, token):
    url = "http://dataservice.accuweather.com/forecasts/v1/%s/%s/%s?apikey=%s&metric=true" \
        % (forecast, period, loc_key, token)
    try:
        with urllib.request.urlopen(url) as f:
            data = json.load(f)
            forecast_date = datetime.now().isoformat()
    except urllib.error.HTTPError as e:
        print(e, e.read())
        raise

    assert forecast in ("hourly", "daily")
    if forecast == "hourly":
        return itertools.chain.from_iterable(( #generator krotek zawierający krotki
            (
                (x["DateTime"], "temperature", x["Temperature"]["Value"], "hour", forecast_date, "AccuWeather"),
                (x["DateTime"], "precipitation_probability", x["PrecipitationProbability"], "hour", forecast_date, "AccuWeather"),
            )
            for x in data
        ))
    if forecast == "daily":
        return itertools.chain.from_iterable((
            (
                (x["Date"], "temperature_min", x["Temperature"]["Minimum"]["Value"], "day", forecast_date, "AccuWeather"),
                (x["Date"], "temperature_max", x["Temperature"]["Maximum"]["Value"], "day", forecast_date, "AccuWeather"),
            )
            for x in data["DailyForecasts"]
        ))

if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        config = tomllib.load(f)

    con = sqlite3.connect(sys.argv[2])

    rows = []

    if sys.argv[3] == "daily":
        rows += fetch_icm("wrf", "d02_XLONG_XLAT", config["ICM"]["coordinates"], "T2", 0, config["ICM"]["api_key"])
        rows += fetch_icm("wrf", "d02_XLONG_XLAT", config["ICM"]["coordinates"], "RAINNC", 0, config["ICM"]["api_key"])
        rows += fetch_aw("daily", "5day", config["AccuWeather"]["locationKey"], config["AccuWeather"]["apiKey"])
    elif sys.argv[3] == "hourly":
        rows += fetch_aw("hourly", "12hour", config["AccuWeather"]["locationKey"], config["AccuWeather"]["apiKey"])

    con.executemany("INSERT INTO Weather(date_value, metric, value, forecast_period, forecast_date, source) VALUES(?, ?, ?, ?, ?, ?)", rows)
    con.commit()