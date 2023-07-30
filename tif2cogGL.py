### Original code from Guillaume Larocque, CSBQ
### Comments from ChatGPT

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

def run_command(command: List[str], timeout: int=600) -> CompletedProcess: 
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