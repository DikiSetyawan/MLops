import requests
import pandas as pd

# API endpoint URL
#url = 'https://covid-19-data.p.rapidapi.com/country?name=italy&format=json'
url_list_of_country = 'https://covid-19-data.p.rapidapi.com/help/countries?format=json'

# API headers (replace with your own key)
headers = {
    "x-rapidapi-host": "covid-19-data.p.rapidapi.com",
    "x-rapidapi-key": "16c352fa05msh2cefee4bdb2bda6p1d8c6ajsnb394ed300f6a"  # Replace with your actual API key
}

countryList = []
covidata = []
# Send GET request
response = requests.get(url_list_of_country, headers=headers)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    for i in data : 
        print(i)
        countryList.append(i['alpha2code'])
    for i in countryList:
        url = f'https://covid-19-data.p.rapidapi.com/country/code?format=json&code={i}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for i in data : 
                print(i)
                covidata.append(i)
        else:
            print(f"Error: API request failed with status code: {response.status_code}")
else:
    print(f"Error: API request failed with status code: {response.status_code}")

