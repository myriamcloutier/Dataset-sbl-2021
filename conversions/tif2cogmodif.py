from doctest import OutputChecker
from shutil import which
from typing import List
from pathlib import Path
import tempfile
from run_command import run_command
import os

def tif2cog(input_paths: List[Path], type: str, value_type: str="category") -> None:
    for input_path in input_paths:
        output_cog_path = input_path.with_suffix("_OUTPUT.tif")

        temp_vrt_path = input_path
    
        if (type=='raw'): 
            #cog_command = ['gdalwarp', '-of', 'COG', '-co', 'COMPRESS=DEFLATE', '-co', 'OVERVIEWS=IGNORE_EXISTING','-wo','NUM_THREADS=4', '-co', 'NUM_THREADS=ALL_CPUS','-multi', temp_vrt_path, output_cog_path]
            cog_command= "gdalwarp -of COG -co COMPRESS=DEFLATE -co NUM_THREADS=ALL_CPUS -co OVERVIEWS=IGNORE_EXISTING -wo NUM_THREADS=4 -multi  %s %s" % (temp_vrt_path, output_cog_path)
        elif (type=='display'):
            # cog_command = ['gdalwarp', '-of', 'COG', '-s_srs', 'EPSG:32198', '-t_srs', 'EPSG:3857', '-tr', '90 90', '-co', 'TILING_SCHEME=GoogleMapsCompatible', '-co', 'COMPRESS=DEFLATE', '-co', 'NUM_THREADS=ALL_CPUS','-co', 'OVERVIEWS=IGNORE_EXISTING', '-wo','NUM_THREADS=4','-multi', temp_vrt_path, output_cog_path]
            cog_command= "gdalwarp -of COG -t_srs EPSG:3857 -co COMPRESS=DEFLATE -co LEVEL=6 -co NUM_THREADS=ALL_CPUS -co OVERVIEWS=IGNORE_EXISTING -wo NUM_THREADS=4 -multi  %s %s" % (temp_vrt_path, output_cog_path)
        elif (type=='display' & value_type=='category'):
            # cog_command = ['gdalwarp', '-of', 'COG', '-s_srs', 'EPSG:32198', '-t_srs', 'EPSG:3857', '-tr', '90 90', '-co', 'TILING_SCHEME=GoogleMapsCompatible', '-co', 'COMPRESS=DEFLATE', '-co', 'NUM_THREADS=ALL_CPUS','-co', 'OVERVIEWS=IGNORE_EXISTING', '-wo','NUM_THREADS=4','-multi', temp_vrt_path, output_cog_path]
            cog_command= "gdalwarp -of COG -t_srs EPSG:3857 -r mode -co COMPRESS=DEFLATE -co LEVEL=6 -co NUM_THREADS=ALL_CPUS -co OVERVIEWS=IGNORE_EXISTING -co RESAMPLING=NEAREST -co WARP_RESAMPLING=NEAREST -co OVERVIEW_RESAMPLING=NEAREST -wo NUM_THREADS=4 -multi  %s %s" % (temp_vrt_path, output_cog_path)
        os.system(cog_command)

        if not output_cog_path.exists():
            raise FileNotFoundError("The COG was not created, see the full logs for more details.")