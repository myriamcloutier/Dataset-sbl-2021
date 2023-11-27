import os
import pandas as pd
from PIL import Image 
from datetime import datetime, timedelta

def get_image_timestamp(image_path):
    try:
        img = Image.open(image_path)
        info = img._getexif()
        if info:
            timestamp = info.get(36867)  # EXIF tag for DateTimeOriginal
            if timestamp:
                return timestamp
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
    return None

def process_folder(folder_path):
    earliest_timestamp = None
    latest_timestamp = None
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".jpg"):
                image_path = os.path.join(root, file)
                timestamp = get_image_timestamp(image_path)
                
                if timestamp:
                    # Parse the timestamp into a datetime object
                    try:
                        timestamp = datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S")
                    except Exception as e:
                        print(f"Error parsing timestamp {timestamp}: {e}")
                        continue  # Skip this file if timestamp parsing fails

                    # Apply 4-hour time offset
                    #timestamp += timedelta(hours=4)

                    if not earliest_timestamp or timestamp < earliest_timestamp:
                        earliest_timestamp = timestamp
                    if not latest_timestamp or timestamp > latest_timestamp:
                        latest_timestamp = timestamp

                    #print(f"Processed {image_path}, Timestamp:{timestamp}")
    
    return earliest_timestamp, latest_timestamp

if __name__ == "__main__":
    # Read the CSV file containing folder paths
    csv_file = "filename_mission_co2_2023.csv"
    df = pd.read_csv(csv_file)
    
    # Create a list to store results
    results = []
    
    # Process each folder path in the DataFrame
    for index, row in df.iterrows():
        folder_path = row["Folder Path"]
        print(f"Processing folder: {folder_path}")
        earliest, latest = process_folder(folder_path)
        
        if earliest and latest:
            results.append({
                "Folder Path": folder_path,
                "Earliest Timestamp": earliest,
                "Latest Timestamp": latest
            })
        else:
            print(f"No JPEG files with valid timestamps found in {folder_path}")
    
    # Create a DataFrame from the results
    results_df = pd.DataFrame(results)
    
    # Convert timestamps to RFC 3339 UTC format
    results_df["Earliest Timestamp"] = pd.to_datetime(results_df["Earliest Timestamp"]).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    results_df["Latest Timestamp"] = pd.to_datetime(results_df["Latest Timestamp"]).dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Save the results DataFrame to an Excel file
    excel_output_file = "timestamps_rgb_co2_2023.xlsx"
    results_df.to_excel(excel_output_file, index=False)
    
    print("Timestamps saved to", excel_output_file)

#if __name__ == "__main__":
 #   root_folder = "F:/Dataset-2021-sbl/missions_drones/2021-09-02-sbl-cloutier-z3-P4RTK-WGS84"
  #  earliest, latest = process_folder(root_folder)
    
  #  if earliest and latest:
   #     print(f"Earliest timestamp: {earliest}")
    #    print(f"Latest timestamp: {latest}")
  #  else:
   #     print("No JPEG files with valid timestamps found.")

