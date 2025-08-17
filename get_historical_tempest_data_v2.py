# creates a csv file and loads it to an S3 bucket then does so again
from dotenv import load_dotenv
import os
import requests
import boto3

load_dotenv()

API_KEY = os.getenv("API_KEY")
DEVICE_ID = os.getenv("DEVICE_ID")
TIME_START = 1752451200
TIME_END = 1752883200
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_PREFIX = os.getenv("S3_PREFIX")

# Construct the URL
url = (
    f"https://swd.weatherflow.com/swd/rest/observations/device/{DEVICE_ID}"
    f"?time_start={TIME_START}&time_end={TIME_END}&format=csv&api_key={API_KEY}"
)

# Send request and get response
response = requests.get(url)

if response.status_code == 200:
    filename = f"tempest_data_{TIME_START}_{TIME_END}.csv"
    
    # Save locally
    with open(filename, "w") as f:
        f.write(response.text)
    print(f"✔️ CSV saved: {filename}")

    # Upload to S3
    s3_key = f"{S3_PREFIX}/{filename}"
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    s3.upload_file(filename, S3_BUCKET, s3_key)
    print(f"✔️ Uploaded to S3: s3://{S3_BUCKET}/{s3_key}")

else:
    print(f"❌ Failed to fetch data: {response.status_code} - {response.text}")