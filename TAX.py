import os
import pickle
import requests
import pandas as pd

# Define the API endpoint and parameters
api_url = 'https://api.census.gov/data/2021/acs/acs5'
params = {
    'get': 'NAME,B01001_001E',  # Requesting the state name and total population estimate
    'for': 'state:*',
    'key': '7f96458e1c960a8411c15c2e298b1b456a4d15ad'
}
cache_filename = 'acs_data.pkl'

# Function to fetch and cache data from the Census API
def fetch_and_cache(api_url, params, cache_filename):
    if os.path.exists(cache_filename):
        print(f"Loading cached data from {cache_filename}")
        with open(cache_filename, 'rb') as f:
            data = pickle.load(f)
    else:
        print("Fetching data from API...")
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an error for a bad response
        data = response.json()
        with open(cache_filename, 'wb') as f:
            pickle.dump(data, f)
    return data

# Fetch the data (either from cache or API)
data = fetch_and_cache(api_url, params, cache_filename)

# Print the column names (first element of the JSON response)
columns = data[0]
print("Column Names:")
print(", ".join(columns))

# Convert the remaining data into a DataFrame and print a preview
df = pd.DataFrame(data[1:], columns=columns)
print("\nDataset Preview:")
print(df.head())
