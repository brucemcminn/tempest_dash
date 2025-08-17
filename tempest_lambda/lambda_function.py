'''
This script executes a GET on the Tempest API and
loads historical weather data to an S3 bucket.
August 5, 2025
'''

def lambda_handler(event, context):
    from datetime import datetime, timedelta, timezone
    import os
    import requests
    import boto3
    import time

    # === CONFIG ===
    LAST_RUN_KEY = "control/last_run.txt"  # Path in S3 bucket for last run date
    CHUNK_DAYS = 5                         # Days per request chunk
    THROTTLE_SECONDS = 4                   # Seconds between uploads to S3

    # === LOAD ENV VARS ===
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    DEVICE_ID = os.getenv("DEVICE_ID")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_PREFIX = os.getenv("S3_PREFIX")  # e.g., "historic_data/raw/"

    # === INIT S3 ===
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # === DETERMINE START/END DATES ===
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=LAST_RUN_KEY)
        last_run_str = obj["Body"].read().decode("utf-8").strip()
        start_date = datetime.fromisoformat(last_run_str)
        print(f"Resuming from last run date: {start_date}")
    except s3.exceptions.NoSuchKey:
        start_date = datetime(2023, 5, 1, tzinfo=timezone.utc)
        print(f"No last_run.txt found in S3 — starting from {start_date}")

    end_date = datetime.now(timezone.utc)
    chunk_duration = timedelta(days=CHUNK_DAYS)
    current_start = start_date
    chunk = 1

    # === FETCH & UPLOAD LOOP ===
    while current_start < end_date:
        current_end = min(current_start + chunk_duration, end_date)
        start_epoch = int(current_start.timestamp())
        end_epoch = int(current_end.timestamp())

        url = (
            f"https://swd.weatherflow.com/swd/rest/observations/device/{DEVICE_ID}"
            f"?time_start={start_epoch}&time_end={end_epoch}&format=csv&api_key={API_KEY}"
        )

        print(f"Chunk {chunk}: {current_start} to {current_end}")
        response = requests.get(url)

        if response.status_code == 200:
            s3_key = f"{S3_PREFIX}tempest_data_{start_epoch}_{end_epoch}.csv"
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=response.text,
                ContentType="text/csv"
            )
            print(f"Uploaded to S3: s3://{S3_BUCKET}/{s3_key}")
        else:
            print(f"Failed to fetch data: {response.status_code} {response.text}")

        current_start = current_end
        chunk += 1
        time.sleep(THROTTLE_SECONDS)

    # === SAVE LAST RUN DATE TO S3 ===
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=LAST_RUN_KEY,
        Body=end_date.isoformat()
    )
    print(f"Updated last run date in S3 to {end_date}")