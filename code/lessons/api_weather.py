# Get the current weather from the free Open-Meteo API (no account needed)
import requests
import wifi

# Change these to your own location (find them on a map site)
LATITUDE = 40.71
LONGITUDE = -74.01

URL = ("https://api.open-meteo.com/v1/forecast"
       "?latitude=" + str(LATITUDE) +
       "&longitude=" + str(LONGITUDE) +
       "&current=temperature_2m,wind_speed_10m")

wifi.connect()

response = requests.get(URL)   # send the GET request
print("Status code:", response.status_code)   # 200 means OK
data = response.json()          # turn the JSON text into a dictionary
response.close()                # always close, to free up memory

current = data["current"]
print("Temperature:", current["temperature_2m"], "°C")
print("Wind speed:", current["wind_speed_10m"], "km/h")
