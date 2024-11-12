from asyncio.windows_events import NULL
import sqlite3
import requests
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_insert_observation_data(db_name, observation_station_code):
    """
    Fetch observation data from the API, parse it, and insert it into the specified database.
    
    Parameters:
    - db_name (str): The name or path of the SQLite database file.
    - observation_station_code (str): The station code to identify the relevant observation data.
    """

    observation_stations_dict = {
        "1200522": "Funchal", "1240971": "Madeira, Funchal, Lido", "1200524": "Porto Santo", 
        "1210765": "Cabo Raso", "1210766": "Barreiro, Lavradio", "1210767": "Pegoes", 
        "6210879": "Portimao (Praia da Rocha)", "1210770": "Setubal", "1200531": "Cabo Carvoeiro", 
        "6213012": "Carregal do Sal (CIM)", 

        "1200533": "Sagres", "6213014": "Mangualde / Chas de Tavares  (CIM)", 
        "1200535": "Lisboa (Geofisico)", "1210776": "Alcacer do Sal, Barrosinha", 
        "6213017": "Penalva do Castelo (CIM)", "6213018": "Sao Pedro do Sul (CIM)", 
        "6213019": "Santa Comba Dao (CIM)", "6213020": "Satao (CIM)", 
        "1200541": "Sines", "6213022": "Vila Nova do Paiva (CIM)", 

        "1210783": "Alvalade", "6213024": "Viseu / Torredeita (CIM)", "1200545": "Porto, Pedras Rubras (Aerodromo)", 
        "1200548": "Coimbra (Aerodromo)", "1210789": "Aljezur", "1210790": "Foia", 
        "1200551": "Viana Castelo, Chafe", "1200554": "Faro (Aerodromo)", 
        "6213011": "Aguiar da Beira (CIM)", "6213618": "Penela / Serra do Espinhal (CIM)", 

        "1200558": "Evora (C.Coordenacao)", "6213021": "Tondela, Caramulinho (CIM)", 
        "1200560": "Viseu (C.Coordenacao)", "1200562": "Beja", "1210803": "Zebreira", 
        "1210806": "Proenca-a-Nova, P.Moitas", "1200567": "Vila Real", 
        "1200568": "Penhas Douradas", "1240820": "Portalegre (cidade)", 
        "1200570": "Castelo Branco", 

        "1200571": "Portalegre", "1210812": "Alvega", "1200575": "Braganca", 
        "1200576": "Braganca (Aerodromo)", "1200579": "Lisboa (G.Coutinho)", 
        "1210824": "Avis, Benavila", "1210826": "Mora", "1210835": "Elvas", 
        "1210837": "Estremoz", "1210840": "Reguengos, S. P. do Corval", 

        "1210788": "Zambujeira", "11217370": "Terceira / Ribeira das Nove (DROTRH)", 
        "11217372": "Terceira / Serra do Cume (DROTRH)", "1210846": "Montemor-O-Novo", 
        "1210847": "Viana do Alentejo", "1210848": "Portel, Oriola", "1240546": "Porto, Serra do Pilar", 
        "1210851": "Amareleja", "6213013": "Castro Daire / Mezio (CIM)", 
        "6213611": "Arganil / Aerodromo (CIM)", 

        "6213612": "Cantanhede / Fonte Dom Pedro (CIM)", "6213613": "Coimbra / Mata de Sao Pedro (CIM)", 
        "6213614": "Gois / Quinta da Ribeira (CIM)", "1210863": "Mertola, Vale Formoso", 
        "1210864": "Castro Verde, N.Corvo", "1210865": "Alcoutim, Mart.Longo", 
        "1210866": "Vila Real de S.Antonio", "1210867": "Castro Marim (RN Sapal)", 
        "6213620": "Oliveira do Hospital (CIM)", "6213621": "Soure (CIM)", 

        "1240566": "Vila Real (Cidade)", "1210874": "Albufeira", "11217225": "Sao Miguel / Sete Cidades (DROTRH)", 
        "1210878": "Portimao (Aerodromo)"
    }
    # URLs for IPMA data
    api_url = "https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json"
    time_right_now = datetime.now()
    observation_station = observation_stations_dict.get(observation_station_code)
    
    if observation_station is None:
        logging.error(f"No such observation station code. Forecast data will not be fetched or stored!")
        return
    try:
        # Connect to the database
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            
            # Fetch data from API
            response = requests.get(api_url)
            if response.status_code == 200:
                dados_estacoes = response.json()
                data_list = []
                
                # Parse and collect relevant data
                for date, data in dados_estacoes.items():
                    if observation_station_code in data:
                        data_list.append({
                            "date": datetime.strptime(date, "%Y-%m-%dT%H:%M").isoformat(),
                            "temperature": float(data[observation_station_code].get("temperatura", 0)),
                            "wind_speed": float(data[observation_station_code].get("intensidadeVentoKM", 0)),
                            "humidity": float(data[observation_station_code].get("humidade", 0)),
                            "pressure": float(data[observation_station_code].get("pressao", 0)),
                            "wind_direction": float(data[observation_station_code].get("idDireccVento", 0))
                        })

                # Sort data by date
                sorted_data_list = sorted(data_list, key=lambda x: x["date"])

                # Insert data into the database
                for data_item in sorted_data_list:
                    # Check for existing entry with the same date
                    cursor.execute("SELECT COUNT(*) FROM IPMAObservations WHERE date = ?", (data_item["date"],))
                    observation_exists = cursor.fetchone()[0]

                    if not observation_exists:
                        cursor.execute('''INSERT OR IGNORE INTO IPMAObservations 
                                          (date, temperature, wind_speed, humidity, pressure, wind_direction)
                                          VALUES (?, ?, ?, ?, ?, ?)''',
                                       (data_item["date"], data_item["temperature"], data_item["wind_speed"],
                                        data_item["humidity"], data_item["pressure"], data_item["wind_direction"]))
                logging.info(f"Observations inserted into the database for station: {observation_station}!")
            else:
                 logging.info(f"Could not reach IPMA database to get observations for station: {observation_station}!")
    except Exception as e:
        logging.error(f"Could not reach IPMA database to get observations data. Error: {e}")

def fetch_and_insert_forecast_data(db_name, city_code):
    """
    Fetches forecast data from the API, checks for existing entries in the database,
    and inserts new forecast data if not already present.
    
    Parameters:
    - db_name (str): The name or path of the SQLite database file.
    - city_code (str): The city code for the IPMA API
    """

    city_dict = {
    "1010500": "Aveiro", "1020500": "Beja", "1030300": "Braga", "1030800": "Guimaraes", "1040200": "Braganca",
    "1050200": "Castelo Branco", "1060300": "Coimbra", "1070500": "Evora", "1080500": "Faro", "1081505": "Sagres",
    "1081100": "Portimao", "1080800": "Loule", "1090700": "Guarda", "1090821": "Penhas Douradas", "1100900": "Leiria",
    "1110600": "Lisboa", "1121400": "Portalegre", "1131200": "Porto", "1141600": "Santarem", "1151200": "Setubal",
    "1151300": "Sines", "1160900": "Viana do Castelo", "1171400": "Vila Real", "1182300": "Viseu", "2310300": "Funchal",
    "2320100": "Porto Santo", "3410100": "Vila do Porto", "3420300": "Ponta Delgada", "3430100": "Angra do Heroismo", "3440100": "Santa Cruz da Graciosa",
    "3450200": "Velas", "3460200": "Madalena", "3470100": "Horta", "3480200": "Santa Cruz das Flores", "3490100": "Vila do Corvo"
    }
    
    time_right_now = datetime.now()
    city = city_dict[city_code]

    if city is None:
        logging.error(f"No such city code. Forecast data will not be fetched or stored!")
        return

    url_previsao = f"https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{city_code}.json"

    try:
        # Fetch data from API
        response = requests.get(url_previsao)
        if response.status_code != 200:
            logging.info(f"Could not reach IPMA database to get forecast for the city of {city}!")
            logging.info("hielo")
            return
        
        dados_previsao = response.json()
        forecast_update_date = dados_previsao["dataUpdate"]
        forecast_data = []
        # Parse each forecast entry
        for data in dados_previsao["data"]:
            forecast_date = data["forecastDate"] + "T00:00:00"

            # Approximate wind speed based on class
            wind_speed_class = int(data["classWindSpeed"])
            wind_speed = {1: 8, 2: 25, 3: 45, 4: 65}.get(wind_speed_class, 0)

            # Append parsed forecast entry
            forecast_data.append({
                "forecastDate": forecast_date,
                "precipitaProb": float(data["precipitaProb"]),
                "tMin": float(data["tMin"]),
                "tMax": float(data["tMax"]),
                "predWindDir": data["predWindDir"],
                "idWeatherType": data["idWeatherType"],
                "classWindSpeed": wind_speed,
                "longitude": float(data["longitude"]),
                "latitude": float(data["latitude"]),
                "classPrecInt": data.get("classPrecInt")
            })

        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            # Check for existing entry with the same update date in Forecast5Days
            cursor.execute("SELECT COUNT(*) FROM IPMAForecast5Days WHERE dataUpdate = ?", (forecast_update_date,))
            exists = cursor.fetchone()[0]

            if not exists:
                forecast_ids = []
                for data in forecast_data:
                    # Insert individual forecast entry and get the inserted ID
                    cursor.execute('''INSERT INTO IPMAForecast (forecastDate, precipitaProb, tMin, tMax, predWindDir, idWeatherType, 
                                      classWindSpeed, longitude, latitude, classPrecInt)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                   (data["forecastDate"], data["precipitaProb"], data["tMin"], data["tMax"], 
                                    data["predWindDir"], data["idWeatherType"], data["classWindSpeed"], 
                                    data["longitude"], data["latitude"], data["classPrecInt"]))
                    
                    # Retrieve the row ID of the inserted forecast and add it to forecast_ids
                    forecast_ids.append(cursor.lastrowid)

                # Insert the 5-day forecast summary with forecast IDs
                cursor.execute('''INSERT INTO IPMAForecast5Days (dataUpdate, ForecastToday, ForecastTomorrow, Forecast2DaysAfter, 
                                      Forecast3DaysAfter, Forecast4DaysAfter)
                                  VALUES (?, ?, ?, ?, ?, ?)''',
                               (forecast_update_date, *forecast_ids[:5]))  # Store up to 5 forecast references
                
            logging.info(f"Forecast data successfully fetched and inserted into the database for the city of {city}!")
    except Exception as e:
        logging.info(f"Could not reach IPMA database to get forecast for the city of {city}: {e}!")