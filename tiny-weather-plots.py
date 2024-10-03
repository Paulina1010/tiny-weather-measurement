

import sqlite3
from datetime import date
from datetime import datetime, timedelta
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import operator

con = sqlite3.connect("db.sqlite")

today = date.today()

#Forecast comparison for 12 hours (for ICM and AccuWeather)
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
    #for time in x:
        #time = datetime.fromisoformat(time)  
    x = [datetime.fromisoformat(time) for time in x]
    

    plt.plot(x, y, label=source)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) #data na stringa, pelna data: '%Y-%m-%d %H:%M'
plt.legend()
plt.gcf().autofmt_xdate()
#plt.xticks(rotation=45)
plt.xlabel('Godzina')
plt.ylabel('Temperatura')
plt.title('Progonoza godzinowa temperatury na dzień %s' % today)
plt.grid(True)

plt.savefig('wykres godzinowy temperatury.png')

#Forecast precipitation (only from ICM)
cur = con.execute("""
        SELECT source, date_value, value
        FROM Weather 
        WHERE forecast_period='hour' AND metric='precipitation' AND date_value LIKE ?
        ORDER BY source, date_value
        """, ("%sT%%" % today,))
plt.figure(figsize=(10, 6))
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
plt.title('Progonoza godzinowa opadów na dzień %s' % today)
plt.grid(True)
bbox = dict(boxstyle='square', lw=2, ec='gray', fc=(0.9, 0.9, .9, .5), alpha=0.5)
#description
plt.gcf().text(0.7,0.8,"<2.5mm/h - lekki opad,              2.5-7.5mm/h - umiarkowany,      >7.5mm/h - silny opad", ha='left', wrap=True, alpha=0.5, bbox=bbox)
#horizontal lines
plt.axhline(y=2.5, color='lightsteelblue')
plt.axhline(y=7.5, color='royalblue')
plt.savefig('wykres godzinowy opadow.png')