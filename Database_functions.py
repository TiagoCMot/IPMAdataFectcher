import sqlite3

def create_tables(db_name):
    """
    Create necessary tables in the SQLite database if they don't already exist.
    
    Parameters:
    - db_name (str): The name or path of the SQLite database file.
    """
    try:
        # Connect to the database
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            
            # Create Observations table
            cursor.execute('''CREATE TABLE IF NOT EXISTS IPMAObservations (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                                date TEXT,
                                temperature REAL,
                                wind_speed REAL,
                                humidity REAL,
                                pressure REAL,
                                wind_direction REAL
                            )''')
            
            # Create  Forecast5Days table
            cursor.execute('''CREATE TABLE IF NOT EXISTS IPMAForecast5Days (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                                dataUpdate TEXT,
                                longitude REAL,
                                latitude REAL,

                                ForecastTodayDate TEXT,
                                ForecastTodayPrecipitaProb REAL,
                                ForecastTodayTMin REAL,
                                ForecastTodayTMax REAL,
                                ForecastTodayPredWindDir TEXT,
                                ForecastTodayIDWeatherType REAL,
                                ForecastTodayClassWindSpeed REAL,
                                ForecastTodayClassPrecInt INTEGER,

                                ForecastTomorrowDate TEXT,
                                ForecastTomorrowPrecipitaProb REAL,
                                ForecastTomorrowTMin REAL,
                                ForecastTomorrowTMax REAL,
                                ForecastTomorrowPredWindDir TEXT,
                                ForecastTomorrowIDWeatherType REAL,
                                ForecastTomorrowClassWindSpeed REAL,
                                ForecastTomorrowClassPrecInt INTEGER,

                                Forecast2DaysAfterDate TEXT,
                                Forecast2DaysAfterPrecipitaProb REAL,
                                Forecast2DaysAfterTMin REAL,
                                Forecast2DaysAfterTMax REAL,
                                Forecast2DaysAfterPredWindDir TEXT,
                                Forecast2DaysAfterIDWeatherType REAL,
                                Forecast2DaysAfterClassWindSpeed REAL,
                                Forecast2DaysAfterClassPrecInt INTEGER,

                                Forecast3DaysAfterDate TEXT,
                                Forecast3DaysAfterPrecipitaProb REAL,
                                Forecast3DaysAfterTMin REAL,
                                Forecast3DaysAfterTMax REAL,
                                Forecast3DaysAfterPredWindDir TEXT,
                                Forecast3DaysAfterIDWeatherType REAL,
                                Forecast3DaysAfterClassWindSpeed REAL,
                                Forecast3DaysAfterClassPrecInt INTEGER,

                                Forecast4DaysAfterDate TEXT,
                                Forecast4DaysAfterPrecipitaProb REAL,
                                Forecast4DaysAfterTMin REAL,
                                Forecast4DaysAfterTMax REAL,
                                Forecast4DaysAfterPredWindDir TEXT,
                                Forecast4DaysAfterIDWeatherType REAL,
                                Forecast4DaysAfterClassWindSpeed REAL,
                                Forecast4DaysAfterClassPrecInt INTEGER

                            )''')
            
            print("Tables created successfully or already exist.")
    except Exception as e:
        print("Error creating tables:", e)

