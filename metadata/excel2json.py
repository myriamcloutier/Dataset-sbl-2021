from fiona import Geometry
import pandas as pd

excel_file = "testjson.xlsx"
df = pd.read_excel(excel_file)

import os
import json
import pystac
import pystac.extensions.projection as proj
import pystac.extensions.scientific as sci
from datetime import datetime
from dateutil import parser
from pystac.extensions.projection import ProjectionExtension

# Create an empty list to store STAC items
items = []

# Define a custom function to preprocess the "coordinates" column
def process_coordinates(coordinates_str):
    # Check if the "coordinates" column is a string
    if isinstance(coordinates_str, str):
        # Remove square brackets and split on comma
        coordinates_str = coordinates_str.replace('[', '').replace(']', '')
        coordinates_list = coordinates_str.split(',')
        
        # Convert the coordinates to float and group them into pairs
        coordinates = [
            list(map(float, coordinates_list[i:i+2])) 
            for i in range(0, len(coordinates_list), 2)
        ]
        return coordinates
    else:
        # Handle other data types or unexpected formats
        return []
    

def process_bbox(data_str):
    # Check if the data column is a string
    if isinstance(data_str, str):
        # Remove all square brackets and split on comma
        data_str = data_str.replace('[', '').replace(']', '')
        data_list = data_str.split(',')
        
        # Convert the data to float
        data = [float(val) for val in data_list]
        return data
    else:
        # Handle other data types or unexpected formats
        return []
    

# Define the directory and filename for the output JSON file
output_directory = "C:/Users/p1177632/Documents/GitHub/Dataset-sbl-2021/"

for index, row in df.iterrows():
    # Define datetime_obj with a default value
    datetime_obj = None
    # Check if the datetime value is valid (not NaT)
    if pd.notna(row['datetime']):
        # Parse datetime string using dateutil
        datetime_str = row['datetime']
        datetime_obj = parser.parse(datetime_str)
    
    # Convert the 'id' value to a string
    item_id = str(row['id'])

    # Process the "coordinates" data using the custom function
    coordinates = process_coordinates(row['coordinate'])

    # Process the bbox data
    bbox = process_bbox(row['bbox'])

    # Create a STAC item for each row
    item = pystac.Item(
        id=item_id, 
        bbox=bbox,
        geometry={
            'type': 'Polygon',
            'coordinates': coordinates
        },
        datetime = datetime_obj,
        properties={
            'title': row['title'],
            'description': row['description'],
            'start_datetime': row['start_datetime'],
            'end_datetime': row['end_datetime'],
            'created': row['created'],
            'updated': row['updated'],
            'platform': row['platform'],
            'instrument': row['instrument'],
            'gsd': row['gsd'],
            'sci:doi' : '10.5281/zenodo.8148479',
            'sci:publication' : 'https://doi.org/10.1101/2023.08.03.548604'
        },
    )
    
     # Create a projection extension object
    projection_extension = ProjectionExtension.ext(item, add_if_missing=True)

    # Set projection information (modify with your actual projection data)
    projection_extension.epsg = 32618

    # Serialize the STAC item as JSON
    item_json = item.to_dict()

    # Define the filename for the JSON file
    item_filename = f"{item_id}.json"
    item_filepath = os.path.join(output_directory, item_filename)

    # Save the STAC item as JSON in the specified directory
    with open(item_filepath, "w") as json_file:
        json.dump(item_json, json_file, indent=4)

    # Close the JSON file
    json_file.close()
