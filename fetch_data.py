import requests
import pandas as pd

# Replace with your ngrok URL or API endpoint
url = "https://e60c-103-47-74-66.ngrok-free.app//users"

# Fetch data from the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Convert JSON data to pandas DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to an Excel file
    df.to_excel("users_data.xlsx", index=False)

    print("Data has been successfully saved to users_data.xlsx")
else:
    print(f"Failed to fetch data, status code: {response.status_code}")

import requests
import pandas as pd

# Replace with your ngrok URL or API endpoint
url = "https://e60c-103-47-74-66.ngrok-free.app//users"

# Fetch data from the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Convert JSON data to pandas DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to an Excel file
    df.to_excel("users_data.xlsx", index=False)

    print("Data has been successfully saved to users_data.xlsx")
else:
    print(f"Failed to fetch data, status code: {response.status_code}")
