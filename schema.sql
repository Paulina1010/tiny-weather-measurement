CREATE TABLE Weather(
    date_value TEXT,
    metric TEXT,
    value REAL,
    forecast_period TEXT,
    forecast_date TEXT,
    source TEXT,
    PRIMARY KEY (date_value, metric, forecast_period, forecast_date, source)
);