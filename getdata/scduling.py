import schedule
import time
import os
import pandas as pd
from get import WeatherData
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('key_opeweath')

iterations = 0
max_iterations = 100

def fetch_and_append_weather():
    global iterations

    if iterations >= max_iterations:
        print("Reached the maximum number of iterations. Exiting.")
        return schedule.CancelJob

    api_key = key
    cities = ['Jakarta', 'Surabaya', 'Palembang', 'Bandung']

    weather_data = WeatherData(api_key)
    new_data = weather_data.get_weather_data_for_cities(cities)
    
    # Define the CSV file path
    file_path = r'D:\project\porto\data\data.csv'
    
    # Check if the file exists
    if os.path.exists(file_path):
        # If it exists, append without writing the header
        new_data.to_csv(file_path, mode='a', header=False, index=False)
    else:
        # If it doesn't exist, create it and write the header
        new_data.to_csv(file_path, mode='w', header=True, index=False)

    print("Appended new data:")
    print(new_data)

    iterations += 1

def start_scheduler():
    # Schedule the task to run every minute
    schedule.every(1).minutes.do(fetch_and_append_weather)

    # Keep the script running
    while iterations < max_iterations:
        schedule.run_pending()
        time.sleep(1)

    print("Finished all scheduled tasks.")

if __name__ == "__main__":
    start_scheduler()