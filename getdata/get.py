import requests
import pandas as pd
import schedule
from datetime import datetime

class WeatherData:
    def __init__(self, api_key):
        self.api_key = api_key

    def load_weather_data(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        return data

    def transform_data(self, data):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df = pd.DataFrame({
            "City": [data['name']],
            "Temperature (C)": [data['main']['temp']],
            "Weather": [data['weather'][0]['description']],
            "Humidity (%)": [data['main']['humidity']],
            "Wind Speed (m/s)": [data['wind']['speed']], 
            "time": [current_time]
        })
        return df

    def get_weather_data_for_cities(self, cities):
        all_data = pd.DataFrame()

        for city in cities:
            data = self.load_weather_data(city)
            if data.get('cod') != 200:
                print(f'City not found or invalid API key for {city}')
            else:
                city_df = self.transform_data(data)
                all_data = pd.concat([all_data, city_df], ignore_index=True)
                

        return all_data
    

    

# Example usage

