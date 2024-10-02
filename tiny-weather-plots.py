#Forecast comparison for 12 hours (now for ICM and AccuWeather)

#Plot for AccuWeather
import sqlite3
from datetime import date
from datetime import datetime
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import operator

con = sqlite3.connect("db.sqlite")

today = date.today()

#draw plot of temperature for today
cur = con.execute("""
        SELECT source, date_value, value
        FROM Weather 
        WHERE forecast_period='hour' AND metric='temperature' AND date_value LIKE ?
        ORDER BY source, date_value
        """, ("%sT%%" % today,))
plt.figure(figsize=(10, 6))
for source, data in groupby(cur, operator.itemgetter(0)):  
    try:
        _, x, y = zip(*data)
    except ValueError:
        x = []
        y = []
    for time in x:
        time = datetime.fromisoformat(time)  
    x = [datetime.fromisoformat(time) for time in x]
    

    plt.plot(x, y, label=source)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) #data na stringa, pelna data: '%Y-%m-%d %H:%M'
plt.legend()
plt.gcf().autofmt_xdate()
#plt.xticks(rotation=45)
plt.xlabel('Godzina')
plt.ylabel('Temperatura')
plt.title('Progonoza godzinowa na dzień %s' % today)
plt.grid(True)

plt.savefig('wykres godzinowy temperatury.png')

#draw for precipitation
cur = con.execute("""
        SELECT source, date_value, value
        FROM Weather 
        WHERE forecast_period='hour' AND metric='precipitation'
        ORDER BY source, date_value
        """)
plt.figure(figsize=(10, 6))
for source, data in groupby(cur, operator.itemgetter(0)):  
    try:
        _, x, y = zip(*data)
    except ValueError:
        x = []
        y = []
    for time in x:
        time = datetime.fromisoformat(time)  
    x = [datetime.fromisoformat(time) for time in x]
    

    plt.plot(x, y, label=source)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.legend()
plt.gcf().autofmt_xdate()
plt.grid(True)

plt.savefig('wykres godzinowy opadow.png')