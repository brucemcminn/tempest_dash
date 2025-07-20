from datetime import datetime, timedelta, timezone
from tabulate import tabulate
import pytz

# Pacific timezone
PST = pytz.timezone("America/Los_Angeles")

# Set your desired starting date
start_date = datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc)
end_date = datetime.now(timezone.utc)

# 5 days in seconds
chunk_duration = timedelta(days=5)

print(f"{'Chunk':<6} {'Start PST':<25} {'End PST':<25} {'Start Epoch':<15} {'End Epoch':<15}")
print("-" * 90)



chunk = 1
current_start = start_date

while current_start < end_date:
    current_end = min(current_start + chunk_duration, end_date)

    # Convert to PST
    pst_start = current_start.astimezone(PST).strftime("%Y-%m-%d %H:%M:%S")
    pst_end = current_end.astimezone(PST).strftime("%Y-%m-%d %H:%M:%S")

    # Convert to epoch seconds
    epoch_start = int(current_start.timestamp())
    epoch_end = int(current_end.timestamp())

    print(f"{chunk:<6} {pst_start:<25} {pst_end:<25} {epoch_start:<15} {epoch_end:<15}")

    # Advance to next chunk
    current_start = current_end
    chunk += 1

