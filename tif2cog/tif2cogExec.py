from pathlib import Path
import csv
from tif2cogfunc import tif2cog

# Defining input paths from CSV file

input_paths = []

with open('geotiff_path.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        input_paths.append(Path(row[0]))

tif2cog(input_paths, suffix="cog", type="raw")

for path in input_paths:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")