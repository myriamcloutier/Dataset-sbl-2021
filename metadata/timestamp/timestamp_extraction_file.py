'''
Extraction of timestamp for individual tif files

Author: Myriam Cloutier

Timestamp is exported in an Excel in RFC 3339 UTC format. 
To make sure the time is in UTC (for Quebec daylight saving time), apply the 4-hour time offset in when defining the time zone offset.
'''

import os
import pandas as pd
from datetime import datetime, timedelta
import pytz
from openpyxl import Workbook

# Define the time zone offset
time_zone_offset_hours = -4  # Adjust this based on your time zone offset
time_zone = pytz.timezone('UTC')

# Function to convert local time to UTC time with offset
def local_to_utc_with_offset(local_time, offset):
    local_time = local_time.replace(tzinfo=None)
    utc_time = local_time - timedelta(hours=offset)
    return time_zone.localize(utc_time)

# Function to extract timestamp from TIF file
def extract_timestamp_from_tif(tif_path):
    timestamp = os.path.getmtime(tif_path)
    return datetime.utcfromtimestamp(timestamp)

# Read the CSV file containing folder paths
csv_file = "filenamescog.csv" # Sepcify the correct csv file
df = pd.read_csv(csv_file)

# Create an Excel workbook and sheet
wb = Workbook()
sheet = wb.active
sheet.append(['File path','RFC3339 UTC Timestamp'])

# Process each TIF file path in the DataFrame
for index, row in df.iterrows():
    tif_path = row["File path"]
    print(f"Processing TIF file: {tif_path}")
    
    if tif_path.lower().endswith(".tif"):
        local_timestamp = extract_timestamp_from_tif(tif_path)
        adjusted_utc_timestamp = local_to_utc_with_offset(local_timestamp, time_zone_offset_hours)
        rfc3339_utc_timestamp = adjusted_utc_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        sheet.append([tif_path, rfc3339_utc_timestamp])
    else:
        print(f"Skipped {tif_path} as it's not a TIF file.")



# Save the Excel file
excel_output_file = "timestamps_cog.xlsx"
wb.save(excel_output_file)

print(f"Timestamps saved to '{excel_output_file}'.")