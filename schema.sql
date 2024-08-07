CREATE TABLE Weather(
    date_value TEXT,
    metric TEXT,
    value REAL,
    forecast_period TEXT,
    forecast_date TEXT,
    load_date TEXT,
    source TEXT,
    PRIMARY KEY (date_value, metric, forecast_period, forecast_date, load_date, source)
);