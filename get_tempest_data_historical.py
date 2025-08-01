from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os
import requests
import boto3
import time

# Load env vars
load_dotenv()
API_KEY = os.getenv("API_KEY")
DEVICE_ID = os.getenv("DEVICE_ID")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_PREFIX = os.getenv("S3_PREFIX")

# Set date range
start_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
end_date = datetime.now(timezone.utc)
chunk_duration = timedelta(days=5)
current_start = start_date
chunk = 1

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

while current_start < end_date:
    current_end = min(current_start + chunk_duration, end_date)
    start_epoch = int(current_start.timestamp())
    end_epoch = int(current_end.timestamp())

    url = (
        f"https://swd.weatherflow.com/swd/rest/observations/device/{DEVICE_ID}"
        f"?time_start={start_epoch}&time_end={end_epoch}&format=csv&api_key={API_KEY}"
    )

    print(f"\n📡 Chunk {chunk}: {current_start} → {current_end}")
    response = requests.get(url)

    if response.status_code == 200:
        s3_key = f"{S3_PREFIX}/tempest_data_{start_epoch}_{end_epoch}.csv"
        s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=response.text)
        print(f"☁️ Uploaded to S3: s3://{S3_BUCKET}/{s3_key}")

    current_start = current_end
    chunk += 1
    time.sleep(1)  # throttle for politeness

print("\n✅ All chunks complete.")
