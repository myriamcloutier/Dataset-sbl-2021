####
# Run functions in stac_functions.R.
# Here is how to use those functions to extract metadata from local tif files.
####

##### To extract the bounding box for a raster

# Load the raster data

load_cube() # This function will return a proxy raster data cube

# Extract raster coordinates

x <- gdalcubes::dimension_values(cube)$x
y <- gdalcubes::dimension_values(cube)$y
raster_coords <- expand.grid(x, y) %>% setNames(c("lon", "lat"))

# Calculate the bounding box

bbox <- points_to_bbox(raster_coords, proj.from = "EPSG:32198")

# bbox will be a numeric vector with xmin, xmax, ymin, and ymax representing the extent of the raster's bounding box.
