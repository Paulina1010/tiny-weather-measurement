import sqlite3
from datetime import date
from datetime import datetime, timedelta
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import operator
import sys

SCALE = 0.8

# Forecast comparison for 12 hours (for ICM and AccuWeather)
def forecast_temperature(date, file_name):
    cur = con.execute("""
            SELECT source, date_value, value
            FROM (
                    SELECT date_value, metric, value, forecast_date, forecast_period, source,
                            row_number() OVER (PARTITION BY date_value ORDER BY forecast_date DESC) AS RN
                    FROM Weather
                    WHERE forecast_period='hour' AND metric='temperature' AND date_value LIKE ?
                ) X
            WHERE X.RN = 1
            ORDER BY source, date_value
            """, ("%sT%%" % today,))
    plt.figure(figsize=(SCALE*10, SCALE*6))

    for source, data in groupby(cur, operator.itemgetter(0)):
        try:
            _, x, y = zip(*data)
        except ValueError:
            x = []
            y = []
        x = [datetime.fromisoformat(time) for time in x]
        plt.plot(x, y, label=source)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.xlabel('Godzina')
    plt.ylabel('Temperatura [°C]')
    plt.title('Progonoza godzinowa temperatury na dzień %s' % today, y=1.05)
    plt.grid(True)
    plt.savefig(file_name, bbox_inches='tight')

# Forecast precipitation (only from ICM)
def forecast_precipitation(date, file_name):
    cur = con.execute("""
            SELECT source, date_value, value
            FROM Weather
            WHERE forecast_period='hour' AND metric='precipitation' AND date_value LIKE ?
            ORDER BY source, date_value
            """, ("%sT%%" % today,))

    plt.figure(figsize=(SCALE*10, SCALE*6))

    for source, data in groupby(cur, operator.itemgetter(0)):
        try:
            _, x, y = zip(*data)
        except ValueError:
            x = []
            y = []
        x = [datetime.fromisoformat(time) for time in x]
        plt.bar(x, y, width=timedelta(hours=0.9), label=source)

    plt.ylim(0,10)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gcf().autofmt_xdate()
    plt.xlabel('Godzina')
    plt.ylabel('Opady [mm/h]')
    plt.title('Progonoza godzinowa opadów na dzień %s' % today, y=1.05)
    plt.grid(True)
    bbox = dict(boxstyle='square', linewidth=1, edgecolor='lightgray', facecolor='white')
    textstr = "<2.5mm/h - lekki opad,\n 2.5-7.5mm/h - umiarkowany, \n>7.5mm/h - silny opad"
    plt.gcf().text(0.62,0.77, textstr, ha='left', color='royalblue', wrap=True, bbox=bbox)
    plt.axhline(y=2.5, color='lightsteelblue')
    plt.axhline(y=7.5, color='royalblue')
    plt.savefig(file_name, bbox_inches='tight')

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: tiny-weather-plots.py DB_PATH KIND PATH", file=sys.stderr)
        exit(1)

    con = sqlite3.connect(sys.argv[1])
    today = date.today()
    if sys.argv[2] == "temp":
        forecast_temperature(today, sys.argv[3])
    if sys.argv[2] == "prec":
        forecast_precipitation(today, sys.argv[3])