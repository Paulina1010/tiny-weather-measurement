# Tiny weather measurement

Tiny weather measurement is weather project designed to extract, transform, and visualize weather data from various sources. The project gathers weather data, stores it in an SQLITE database, and generates plots to provide a weather forecast focused on temperature and precipitation for the current day.

The main goal of this project is to compare weather forecasts from different sources and evaluate their accuracy. Future development plans include integrating additional data sources and measuring actual temperature values to assess forecast precision.

1. Data Extraction

	The project collects weather data from two sources, AccuWeather and ICM, using their respective APIs:
	- **ICM Data**: Loaded daily to gather information on temperature and precipitation.
	- **AccuWeather Data**:
	    - Daily data for 5-day minimum and maximum temperature forecasts.
	    - Hourly data for temperature and precipitation probability.
2. Data storage

	Extracted data is stored in an SQLite database.
3. Data Visualization

	The project generates plots displaying forecasted temperature and precipitation based on the collected data.

## Usage
1. Clone or download the project repository.
2. Configure API keys.
	To access the weather data, register on the [AccuWeather API](https://developer.accuweather.com) website and request access to their API. Then, sign up on [ICM API](https://api.meteo.pl/) and purchase access to their API. Once you have obtained both API keys, add your AccuWeather and ICM credentials to the `config.toml` file.
	*Ensure this file is not uploaded to the repository for security purposes.*
3. Create database with table.
```sh
sqlite3 db.sqlite < schema.sql
```
4. Run the script as presented below.
```sh
# load daily data
# python tiny-weather-load.py config_file database_file daily
python tiny-weather-load.py config.toml db.sqlite daily

# load hourly data
python tiny-weather-load.py config.toml db.sqlite hourly

# generate temperature forecast plot
# python tiny-weather-plots.py db_source temp file_name
python tiny-weather-plots.py db.sqlite temp public/temp.svg

# generate precipitation forecast plot
python tiny-weather-plots.py db.sqlite prec public/prec.svg
```
Running `tiny-weather-load.py` will extract data from AccuWeather and ICM APIs and load it into the SQLITE database. Running `tiny-weather-plots.py` will generate plots visualizing forecasted temperature and precipitation for the current day.

You can also use CRON to extract data and generate charts on a regular basis.

## Objectives
The primary goal of this project is to compare weather forecasts from different sources and analyze their reliability. Future goals include:
- Adding more data sources.
- Measuring real-time temperature values.
- Visualizing the accuracy of the forecasts with comparison plots.

## Contributing
This project was done as part of a data engineering skills exercise, it is fully working, but if anyone would like to improve this project then they can send a pull request.
Report bugs on the [issue tracker](https://github.com/Paulina1010/tiny-weather-measurement/issues).

## License
MIT, see [LICENSE](LICENSE)


