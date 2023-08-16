import os
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

def process_folder(folder_path):
    earliest_timestamp = None
    latest_timestamp = None
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".jpg"):
                image_path = os.path.join(root, file)
                timestamp = get_image_timestamp(image_path)
                
                if timestamp:
                    if not earliest_timestamp or timestamp < earliest_timestamp:
                        earliest_timestamp = timestamp
                    if not latest_timestamp or timestamp > latest_timestamp:
                        latest_timestamp = timestamp
    
    return earliest_timestamp, latest_timestamp

if __name__ == "__main__":
    root_folder = "F:/Dataset-2021-sbl/2021-09-02-sbl-cloutier-z3-P4RTK-WGS84"
    earliest, latest = process_folder(root_folder)
    
    if earliest and latest:
        print(f"Earliest timestamp: {earliest}")
        print(f"Latest timestamp: {latest}")
    else:
        print("No JPEG files with valid timestamps found.")

