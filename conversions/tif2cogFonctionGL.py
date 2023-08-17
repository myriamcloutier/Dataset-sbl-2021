### Original code from Guillaume Larocque, CSBQ

# Defining two functions to run subprocess commands and create COGs from TIFF files

from subprocess import run, CalledProcessError, CompletedProcess # for running subprocess commands and hangling their outputs
from shutil import which # to check if a given executable (command) exists in the system's PATH
from typing import List # provides type hinting for the function arguments
from pathlib import Path # provides support for working with file paths
import tempfile # used to create temporary files and directory


'''
The `run_command` function takes a `command` (a list of strings representing the subprocess command and its arguments) and an optional `timeout` as input.

It runs the provided subprocess command using the `run` function from the `subprocess` module, capturing the output of the command.

If the command completes successully, it logs the successful command exectution and returns the `CompletedProcess` object. If not, it catches the `CalledProcessError`, performs some logging operations (omitted the code with `...` and raises an exception with relevant information).

It checks if the command's executable is available in the system's PATH using the `which` function from the `shutil` module. If the executable is not found, it raises a `RuntimeError`.
'''

def run_command(command: List, timeout: int=600) -> CompletedProcess:
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



'''
The `tif2cog` function takes three arguments: `input_paths` (a list of `Path` objects representing input TIFF files), `output_cog_path` (a `Path` object representing the output COG file path), and `type` (a string indicating the type of COG to create).

If the length of `input_paths` is greater than 1, it creates a temporary virtual raster (VRT) file using the `gdalbuildvrt` commant (from GDAL) with the `-separate` option. The VRT is used to combine multiple input TIFF files into a single raster stack.

If the length of `input_paths` is 1, it assumes that `input_paths` contains the path to the existing VRT file.



'''

def tif2cogGL(input_paths: List[Path], output_cog_path: Path, type: str) -> None:
    
    if (len(input_paths) > 1):
        temp_vrt_path = (Path(tempfile.gettempdir()) / next(tempfile._get_candidate_names())).with_suffix(".vrt")
        vrt_command = ["gdalbuildvrt", "-separate", temp_vrt_path, *input_paths]
        run_command(vrt_command)
    else:
        temp_vrt_path = input_path[0]
    
    if (type=='raw'): 
        cog_command = ['gdalwarp', '-of', 'COG', '-co', 'COMPRESS=DEFLATE', temp_vrt_path, output_cog_path]
    elif (type=='display'):
        cog_command = ['gdalwarp', '-of', 'COG', '-co', 'TILING_SCHEME=GoogleMapsCompatible', '-co', 'COMPRESS=DEFLATE', temp_vrt_path, output_cog_path]

    run_command(cog_command)

    if not output_cog_path.exists():
        raise FileNotFoundError("The COG was not created, see the full logs for more details.")


