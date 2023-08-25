import os
import pandas as pd
from PIL import Image 

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

def process_file_paths(file_paths):
    data = []

    for image_path in file_paths:
        timestamp = get_image_timestamp(image_path)
        if timestamp:
            data.append({"File Path": image_path, "Timestamp": timestamp})

    return data

#if __name__ == "__main__":
    # Read the CSV file containing file paths CHANGE FOR CSV CONTAINING PATH TO PHOTOS, NOT ORTHOS
    csv_file = "filenamesrgb_TS.csv"
    df = pd.read_csv(csv_file)

    # Get a list of file paths from the DataFrame
    file_paths = df["File Path"].tolist()

    # Process file paths and create a list of dictionaries
    result_data = process_file_paths(file_paths)

    # Create a DataFrame from the list of dictionaries
    result_df = pd.DataFrame(result_data)

    # Display the DataFrame
    print(result_df)

#def process_folder(folder_path):
 #   earliest_timestamp = None
  #  latest_timestamp = None
    
   # for root, _, files in os.walk(folder_path):
    #    for file in files:
     #       if file.lower().endswith(".jpg"):
      #          image_path = os.path.join(root, file)
       #         timestamp = get_image_timestamp(image_path)
                
        #        if timestamp:
         #           if not earliest_timestamp or timestamp < earliest_timestamp:
          #              earliest_timestamp = timestamp
           #         if not latest_timestamp or timestamp > latest_timestamp:
            #            latest_timestamp = timestamp
    
    #return earliest_timestamp, latest_timestamp

if __name__ == "__main__":
    root_folder = "F:/Dataset-2021-sbl/2021-09-02-sbl-cloutier-z3-P4RTK-WGS84"
    earliest, latest = process_folder(root_folder)
    
    if earliest and latest:
        print(f"Earliest timestamp: {earliest}")
        print(f"Latest timestamp: {latest}")
    else:
        print("No JPEG files with valid timestamps found.")

