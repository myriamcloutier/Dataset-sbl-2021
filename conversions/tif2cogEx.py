from pathlib import Path # provides support for working with file paths
#from tif2cogFonctionGL import tif2cogGL, run_command
#from tif2cog import tif2cog
from tif2cogmodif import tif2cog

# Defining input paths
# CHANGE TO PATH IN LEFODATA
input_paths = [
    Path("F:\Dataset-2021-sbl\\2021-05-28\zone1\\2021-05-28-sbl-z1-rgb-cog.tif"),
    Path("F:\Dataset-2021-sbl\\2021-05-28\zone2\\2021-05-28-sbl-z2-rgb-cog.tif"),
    Path("F:\Dataset-2021-sbl\\2021-05-28\zone3\\2021-05-28-sbl-z3-rgb-cog.tif")
]

#input_paths = [
#    Path("\\lefodata\home\data-MSc-cloutier-2021\orthomosaics\quebec_tree_dataset\2021-05-28\2021-05-28-sbl-cloutier-z1-UTM18-MS"),
 #   Path("\\lefodata\home\data-MSc-cloutier-2021\orthomosaics\quebec_tree_dataset\2021-05-28\2021-05-28-sbl-cloutier-z2-UTM18-MS")
  #  Path("\\lefodata\home\data-MSc-cloutier-2021\orthomosaics\quebec_tree_dataset\2021-05-28\2021-05-28-sbl-cloutier-z3-UTM18-MS")
#]

# Defining output path
#output_cog_path = Path("F:\Dataset-2021-sbl\\2021-05-28\zone1\\2021-05-28-sbl-z1-rgb-cog-OUTPUT.tif")

tif2cog(input_paths, type="raw")

#for path in input_paths:
 #   if not path.exists():
  #      raise FileNotFoundError(f"Input file not found: {path}")