from pathlib import Path
import csv
from tif2cogmodif import tif2cog

# Defining input paths from CSV file

input_paths = []

with open('geotiff_path.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        input_paths.append(Path(row[0]))


#input_paths = [
 #   Path("F:\Dataset-2021-sbl\\2021-05-28\zone1\\2021-05-28-sbl-z1-rgb.tif"),
 #   Path("F:\Dataset-2021-sbl\\2021-05-28\zone2\\2021-05-28-sbl-z2-rgb.tif"),
  #  Path("F:\Dataset-2021-sbl\\2021-05-28\zone3\\2021-05-28-sbl-z3-rgb.tif")
#]

tif2cog(input_paths, suffix="cog", type="raw")

for path in input_paths:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")