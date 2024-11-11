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
            cursor.execute('''CREATE TABLE IF NOT EXISTS Observations (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT,
                                temperature REAL,
                                wind_speed REAL,
                                humidity REAL,
                                pressure REAL,
                                wind_direction REAL
                            )''')
            
            # Create Forecast5Days table
            cursor.execute('''CREATE TABLE IF NOT EXISTS Forecast5Days (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                dataUpdate TEXT,
                                ForecastToday INTEGER,
                                ForecastTomorrow INTEGER,
                                Forecast2DaysAfter INTEGER,
                                Forecast3DaysAfter INTEGER,
                                Forecast4DaysAfter INTEGER
                            )''')
            
            # Create Forecast table
            cursor.execute('''CREATE TABLE IF NOT EXISTS Forecast (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                forecastDate TEXT,
                                precipitaProb REAL,
                                tMin REAL,
                                tMax REAL,
                                predWindDir TEXT,
                                idWeatherType INTEGER,
                                classWindSpeed INTEGER,
                                longitude REAL,
                                latitude REAL,
                                classPrecInt INTEGER
                            )''')
            
            print("Tables created successfully or already exist.")
    except Exception as e:
        print("Error creating tables:", e)

