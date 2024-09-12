#Forecast comparison for 12 hours (now for ICM and AccuWeather)

#Plot for AccuWeather

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

accuweather_data = con.execute("SELECT date_value, value FROM Weather WHERE forecast_period='hour' AND source='AccuWeather' ORDER BY date_value")
accuweather_data = accuweather_data.fetchall()

accuweather_x, accuweather_y = zip(*accuweather_data)
accuweather_x = [datetime.fromisoformat(x) for x in accuweather_x]
print(accuweather_x)
print(accuweather_y)


plt.figure(figsize=(10, 6))
plt.plot(accuweather_x, accuweather_y, label='AccuWeather')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M')) #data na stringa
plt.legend()
plt.gcf().autofmt_xdate()
#plt.xticks(rotation=45)
plt.grid(True)

plt.savefig('wykres_AccuWeather.png')

#res = con.execute("SELECT value, date_value, source FROM Weather WHERE forecast_period='hour' AND source='AccuWeather' UNION SELECT * FROM (SELECT value, date_value, source FROM Weather WHERE forecast_period='hour' AND source='ICM' ORDER BY date_value LIMIT 12) ORDER BY date_value")