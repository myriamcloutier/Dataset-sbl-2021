from pathlib import Path # provides support for working with file paths
#from tif2cogFonctionGL import tif2cogGL, run_command
from tif2cog import tif2cog 


# Defining input paths
input_paths = [
    Path("F:\Dataset-2021-sbl\\2021-05-28\zone1\\2021-05-28-sbl-z1-rgb-cog.tif"),
    Path("F:\Dataset-2021-sbl\\2021-05-28\zone2\\2021-05-28-sbl-z2-rgb-cog.tif"),
    Path("F:\Dataset-2021-sbl\\2021-05-28\zone3\\2021-05-28-sbl-z3-rgb-cog.tif")
]

# Defining output path
output_cog_path = Path("F:\Dataset-2021-sbl\\2021-05-28\zone1\\2021-05-28-sbl-z1-rgb-cog-OUTPUT.tif")

tif2cogGL(input_paths, output_cog_path, type="raw")

for path in input_paths:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
