### This script is used to extract timestamps from LAZ files ###

'''
Extraction of timestamp for individual .laz files

Author: Myriam Cloutier

Timestamp is exported in an Excel in RFC 3339 UTC format. 
To make sure the time is in UTC (for Quebec daylight saving time), apply the 4-hour time offset in when defining the time zone offset.
'''


import os
import struct
import datetime
import pytz
import pandas as pd
from openpyxl import Workbook

# Define the time zone offset
time_zone_offset_hours = -4  # Adjust this based on your time zone offset
time_zone = pytz.timezone('UTC')

# Function to convert local time to UTC time with offset
def local_to_utc_with_offset(local_time, offset):
    local_time = local_time.replace(tzinfo=None)
    utc_time = local_time - datetime.timedelta(hours=offset)
    return time_zone.localize(utc_time)

# Function to extract timestamp from LAZ file
def extract_timestamp_from_laz(laz_path):
    # Open the LAZ file in binary mode
    with open(laz_path, "rb") as f:
        # Read the header size (8 bytes) and skip to the creation date field (92 bytes into the header)
        f.seek(8 + 92)
        
        # Read the creation date (8 bytes) as little-endian unsigned long long
        creation_date_bytes = f.read(8)
        creation_date_int = struct.unpack("<Q", creation_date_bytes)[0]
        
        # Adjust the creation date to account for the correct epoch time (January 1, 1601)
        epoch_adjusted_date_int = creation_date_int + 116444736000000000
        
        # Convert the adjusted creation date to a Unix timestamp (seconds since 1970)
        timestamp = epoch_adjusted_date_int / 10000000  # Convert 100-nanosecond intervals to seconds
        return timestamp

# Read the CSV file containing file paths
csv_file = "filenamescopc.csv"  # Replace with your CSV file
df = pd.read_csv(csv_file)

# Create a new DataFrame to store results
#results_df = pd.DataFrame(columns=["File path", "RFC3339 UTC Timestamp"])

# Create an Excel workbook and sheet
wb = Workbook()
sheet = wb.active
sheet.append(['File path','RFC3339 UTC Timestamp'])

# Process each file path in the DataFrame
for index, row in df.iterrows():
    file_path = row["File path"]
    print(f"Processing file: {file_path}")
    
    if file_path.lower().endswith(".laz"):
        timestamp = extract_timestamp_from_laz(file_path)
        
        # Handle large timestamps by splitting them into seconds and microseconds components
        seconds = timestamp // 1000000  # Convert nanoseconds to seconds
        microseconds = int(round(timestamp % 1000000))  # Round and convert to integer
        
        # Create a datetime object from the components
        local_timestamp = datetime.datetime.utcfromtimestamp(seconds)
        local_timestamp = local_timestamp.replace(microsecond=microseconds)
        
        adjusted_utc_timestamp = local_to_utc_with_offset(local_timestamp, time_zone_offset_hours)
        rfc3339_utc_timestamp = adjusted_utc_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        sheet.append([file_path, rfc3339_utc_timestamp])
        #results_df = results_df.append({"File path": file_path, "RFC3339 UTC Timestamp": rfc3339_utc_timestamp}, ignore_index=True)
    else:
        print(f"Skipped {file_path} as it's not a LAZ file.")

# Save the results to a new CSV file
#results_csv = "timestamps_copc.csv"  # Replace with your desired output file name
#results_df.to_csv(results_csv, index=False)

#print("Timestamp extraction completed. Results saved to", results_csv)


# Save the Excel file
excel_output_file = "timestamps_copc.xlsx"
wb.save(excel_output_file)

print(f"Timestamps saved to '{excel_output_file}'.")