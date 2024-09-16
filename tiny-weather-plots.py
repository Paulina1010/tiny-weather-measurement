#Forecast comparison for 12 hours (now for ICM and AccuWeather)

#Plot for AccuWeather
import sqlite3
from datetime import datetime
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

con = sqlite3.connect("db.sqlite")

sources = ["ICM", "AccuWeather"]
for source in sources:
    cur = con.execute("""
            SELECT date_value, value
            FROM Weather 
            WHERE forecast_period='hour' AND source=? 
            ORDER BY source, date_value
            LIMIT 12
            """, (source,))
    
    data_x, data_y = zip(*cur)
    for x in data_x:
        x = datetime.fromisoformat(x)  
    data_x = [datetime.fromisoformat(x) for x in data_x]
    print(data_x)
    print(data_y)   
    
    
   
