# -*- coding: utf-8 -*-
import requests
import sqlite3
from datetime import datetime
from Database_functions import create_tables
from IPMA_functions import fetch_and_insert_observation_data,fetch_and_insert_forecast_data
# Database name
database_name = 'ipma_data.db'

# IPMA codes
observation_station_code = "1210770"  # Observation station near Setúbal, Portugal
city_code = "1151200"  # IPMA city code for Setúbal, Portugal


# Connect to SQLite database
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

create_tables(database_name)
fetch_and_insert_observation_data(database_name, observation_station_code)
fetch_and_insert_forecast_data(database_name,city_code)
# Commit changes and close the database connection
conn.commit()
conn.close()

"""Database Schema
+--------------------+
|    Observations    |          # Stores real-time weather data observed at specific times
+--------------------+
| id: INTEGER PK     |          # Unique ID for each observation record (primary key)
| date: TEXT         |          # Date and time of observation
| temperature: REAL  |          # Temperature reading at the time of observation
| wind_speed: REAL   |          # Wind speed at the time of observation
| humidity: REAL     |          # Humidity level at the time of observation
| pressure: REAL     |          # Atmospheric pressure at the time of observation
| wind_direction: REAL |        # Wind direction at the time of observation
+--------------------+

+---------------------+
|    Forecast5Days    |      # Stores daily forecasts for the next five days, referencing individual forecasts
+---------------------+
| id: INTEGER PK      |      # Unique ID for each 5-day forecast summary (primary key)
| dataUpdate: TEXT    |      # Date and time when the forecast data was updated
| ForecastToday: INTEGER FK -> Forecast.id | # Forecast ID for today's forecast
| ForecastTomorrow: INTEGER FK -> Forecast.id | # Forecast ID for tomorrow's forecast
| Forecast2DaysAfter: INTEGER FK -> Forecast.id | # Forecast ID for the day after tomorrow
| Forecast3DaysAfter: INTEGER FK -> Forecast.id | # Forecast ID for three days after
| Forecast4DaysAfter: INTEGER FK -> Forecast.id | # Forecast ID for four days after
+---------------------+

+--------------------+
|     Forecast       |          # Stores detailed forecast data for individual days
+--------------------+
| id: INTEGER PK     |          # Unique ID for each daily forecast record (primary key)
| forecastDate: TEXT |          # Date of the forecast
| precipitaProb: REAL|          # Probability of precipitation
| tMin: REAL         |          # Minimum temperature forecasted
| tMax: REAL         |          # Maximum temperature forecasted
| predWindDir: TEXT  |          # Predicted wind direction
| idWeatherType: INTEGER |      # ID for the type of weather (e.g., sunny, rainy)
| classWindSpeed: INTEGER |     # Classification of wind speed (e.g., light, moderate)
| longitude: REAL    |          # Longitude of the forecasted location
| latitude: REAL     |          # Latitude of the forecasted location
| classPrecInt: INTEGER |       # Intensity classification for precipitation (if available)
+--------------------+
"""