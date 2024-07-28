import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
from typing import Dict

class WeatherForecaster:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.models = {}

    def prepare_data(self):
        self.data['time'] = pd.to_datetime(self.data['time'])
        self.data['time_ordinal'] = self.data['time'].apply(lambda x: x.toordinal())

    def train_models(self):
        cities = self.data['City'].unique()

        for city in cities:
            city_data = self.data[self.data['City'] == city]
            
            X = city_data[['time_ordinal']]
            y_temp = city_data['Temperature (C)']
            y_humidity = city_data['Humidity (%)']
            y_wind_speed = city_data['Wind Speed (m/s)']
            
            model_temp = self._train_model(X, y_temp)
            model_humidity = self._train_model(X, y_humidity)
            model_wind_speed = self._train_model(X, y_wind_speed)
            
            self.models[city] = {
                'temp_model': model_temp,
                'humidity_model': model_humidity,
                'wind_speed_model': model_wind_speed
            }

    def _train_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        print(f"Model MAE: {mae}")
        return model

    def save_models(self, path: str):
        for city, models in self.models.items():
            for model_name, model in models.items():
                model_filename = f"{path}/{city}_{model_name}.joblib"
                joblib.dump(model, model_filename)
                print(f"Saved {model_name} model for {city} to {model_filename}")

    def load_models(self, path: str, cities: list):
        for city in cities:
            self.models[city] = {}
            for model_type in ['temp_model', 'humidity_model', 'wind_speed_model']:
                model_filename = f"{path}/{city}_{model_type}.joblib"
                self.models[city][model_type] = joblib.load(model_filename)
                print(f"Loaded {model_type} model for {city} from {model_filename}")

    def forecast(self, city: str, future_date: pd.Timestamp) -> Dict[str, float]:
        if city not in self.models:
            raise ValueError(f"No model found for city: {city}")

        future_date_ordinal = future_date.toordinal()
        temp = self.models[city]['temp_model'].predict(np.array([[future_date_ordinal]]))[0]
        humidity = self.models[city]['humidity_model'].predict(np.array([[future_date_ordinal]]))[0]
        wind_speed = self.models[city]['wind_speed_model'].predict(np.array([[future_date_ordinal]]))[0]

        return {
            'Temperature (C)': temp,
            'Humidity (%)': humidity,
            'Wind Speed (m/s)': wind_speed
        }

# Sample data
data = {
    'City': ['Jakarta', 'Surabaya', 'Palembang', 'Bandung'],
    'Temperature (C)': [31.35, 29.97, 33.53, 25.75],
    'Weather': ['haze', 'few clouds', 'scattered clouds', 'scattered clouds'],
    'Humidity (%)': [54, 66, 45, 65],
    'Wind Speed (m/s)': [3.09, 5.66, 2.90, 1.41],
    'time': ['2024-07-28 17:03:40', '2024-07-28 17:03:40', '2024-07-28 17:03:41', '2024-07-28 17:03:41']
}

# Create DataFrame
df = pd.DataFrame(data)

# Create and use the forecaster
forecaster = WeatherForecaster(df)
forecaster.prepare_data()
forecaster.train_models()

# Save models
forecaster.save_models('models')

# Load models (example)
# forecaster.load_models('models', ['Jakarta', 'Surabaya', 'Palembang', 'Bandung'])

# Example of forecasting
future_date = pd.Timestamp('2024-07-29')
for city in df['City'].unique():
    forecast = forecaster.forecast(city, future_date)
    print(f"Forecast for {city} on {future_date.date()}: {forecast}")
