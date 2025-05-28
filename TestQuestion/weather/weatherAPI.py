def CodeToIMG(Code,time):
	import json
	with open("weather/descriptions.json", "r+") as f:
		js = json.load(f)
	DayTime="night" if time>22 or time<5 else "day"
	js = js.get(str(Code)).get(DayTime)
	return [js.get("image"),js.get("description")]

def GetCoords(City):
	import json
	with open("weather/cities.json","r+",encoding="UTF-8") as f:
		coords = json.load(f).get(City)
		print(coords)
	return coords

def API(City):
	import openmeteo_requests
	from datetime import datetime
	import requests_cache
	from retry_requests import retry


	table_data=[]

	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)
	coords = GetCoords(City)
	if coords != None:

		# Make sure all required weather variables are listed here
		# The order of variables in hourly or daily is important to assign them correctly below
		url = "https://api.open-meteo.com/v1/forecast"
		params = {
			"latitude": coords["lat"],
			"longitude": coords["lon"],
			"hourly": ["temperature_2m", "weather_code"],
			"timezone": "auto",
			"forecast_days": 7
		}
		responses = openmeteo.weather_api(url, params=params)
		# Process first location. Add a for-loop for multiple locations or weather models
		response = responses[0]
		# print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
		# print(f"Elevation {response.Elevation()} m asl")
		# print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
		# print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

		# Process hourly data. The order of variables needs to be the same as requested.
		hourly = response.Hourly()
		hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
		hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()

		times = range(hourly.Time(),hourly.TimeEnd(),3600)
		for i in range(len(times)):
			table_data.append([datetime.fromtimestamp(times[i]).strftime('%d-%m-%Y\n%H:%M'),hourly_temperature_2m[i],CodeToIMG(int(hourly_weather_code[i]),int(datetime.fromtimestamp(times[i]).strftime('%H')))])

		# hourly_data = {"date": pd.date_range(
		# 	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		# 	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		# 	freq = pd.Timedelta(seconds = hourly.Interval()),
		# 	inclusive = "left"
		# )}
		#
		# hourly_data["temperature_2m"] = hourly_temperature_2m
		# hourly_data["weather_code"] = hourly_weather_code
		#
		# hourly_dataframe = pd.DataFrame(data = hourly_data)
		# print(hourly_dataframe)
	return table_data