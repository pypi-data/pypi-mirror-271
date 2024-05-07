import requests

class WeatherSDK:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather_by_city_name(self, city_name):
        url = f"{self.base_url}?q={city_name}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_weather_by_coordinates(self, lat, lon):
        url = f"{self.base_url}?lat={lat}&lon={lon}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def weather_timestamp(self, lat, lon, time):
        url = f"{self.base_url}?lat={lat}&lon={lon}&dt={time}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None


    def daily_aggregation(self, lat, lon,date,tz):
        url = f"{self.base_url}?lat={lat}&lon={lon}&date={date}&date={date}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None