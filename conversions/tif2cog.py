### 

from subprocess import run, CalledProcessError, CompletedProcess # for running subprocess commands and hangling their outputs
from shutil import which # to check if a given executable (command) exists in the system's PATH
from typing import List # provides type hinting for the function arguments
from pathlib import Path # provides support for working with file paths
import tempfile # used to create temporary files and directory


def execute_command(command: List[str], timeout: int=600) -> CompletedProcess:
    """Run a subprocess command with error handling and logging functionality.
    """
    process = run(command, capture_output=True, timeout=timeout)

    try:
        process.check_returncode()
        # Log successful command...
        return process

    except CalledProcessError as e:
        ...
        # Send (process.returncode, process.stderr) to logging.
        if which(command[0]) is None:
            raise RuntimeError(f"{command[0]} was not found, is it installed and on the path?")
        else:
            raise ...
        



def tif2cog(input_paths: List[Path], output_cog_path: Path, type: str) -> None:
    temp_vrt_path = None
    
    #if (len(input_paths) > 1):
    temp_vrt_path = (Path(tempfile.gettempdir()) / next(tempfile._get_candidate_names())).with_suffix(".vrt")
    vrt_command = ["gdalbuildvrt", "-separate", temp_vrt_path, *input_paths]
    execute_command(vrt_command)
    #else:
    #    temp_vrt_path = input_path[0]
    
    if (type=='raw'): 
        cog_command = ['gdalwarp', '-of', 'COG', '-co', 'COMPRESS=DEFLATE', temp_vrt_path, output_cog_path]
    elif (type=='display'):
        cog_command = ['gdalwarp', '-of', 'COG', '-co', 'TILING_SCHEME=GoogleMapsCompatible', '-co', 'COMPRESS=DEFLATE', temp_vrt_path, output_cog_path]

    execute_command(cog_command)

    if not output_cog_path.exists():
        raise FileNotFoundError("The COG was not created, see the full logs for more details.")

# Defining input paths
input_paths = [
    Path("F:\Dataset-2021-sbl\2021-05-28\zone1\2021-05-28-sbl-z1-rgb-cog.tif"),
    Path("F:\Dataset-2021-sbl\2021-05-28\zone2\2021-05-28-sbl-z2-rgb-cog.tif"),
    Path("F:\Dataset-2021-sbl\2021-05-28\zone3\2021-05-28-sbl-z3-rgb-cog.tif")
]

# Defining output path
output_cog_path = Path("F:\Dataset-2021-sbl\2021-05-28\zone1\2021-05-28-sbl-z1-rgb-cog-OUTPUT.tif")

tif2cog(input_paths, output_cog_path, type="raw")