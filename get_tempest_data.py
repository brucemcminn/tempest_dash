import requests

# Replace with your actual token
API_KEY = "your_tempest_token_here"
DEVICE_ID = "265233"
TIME_START = 1750662060
TIME_END = 1750921260

# Construct the URL
url = (
    f"https://swd.weatherflow.com/swd/rest/observations/device/{DEVICE_ID}"
    f"?time_start={TIME_START}&time_end={TIME_END}&format=csv&api_key={API_KEY}"
)

# Send request and get response
response = requests.get(url)

# Check and save
if response.status_code == 200:
    filename = f"tempest_data_{TIME_START}_{TIME_END}.csv"
    with open(filename, "w") as f:
        f.write(response.text)
    print(f"✔️ Data saved to {filename}")
else:
    print(f"❌ Failed to fetch data: {response.status_code} - {response.text}")