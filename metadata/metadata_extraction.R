####
# Run functions in stac_functions.R.
# Here is how to use those functions to extract metadata from local tif files.
####

library("gdalcubes")
library("rstac")
library("raster")

##### To extract the bounding box for a raster

# Load and read the raster data

raster_file <- "path/to/tif"
r <- raster(raster_file)


# Get the bounding box using points_to_bbox function

bbox <- points_to_bbox(as.data.frame(extent(r)), buffer = 0, proj.from = projection(r))

# bbox <- points_to_bbox(raster_coords, proj.from = "EPSG:32198")

# bbox will be a numeric vector with xmin, xmax, ymin, and ymax representing the extent of the raster's bounding box.

print(bbox)



#### To extract the bounding box in a loop

# Function to calculate bounding box for a single raster
get_raster_bbox <- function(raster_file) {
  r <- raster(raster_file)
  bbox <- points_to_bbox(as.data.frame(extent(r)), buffer = 0, proj.from = projection(r))
  return(bbox)
}

# List of raster file paths
raster_files <- c("path/to/1.tif", "path/to/2.tif")

# Apply the function to get bounding box for each raster
bbox_list <- lapply(raster_files, get_raster_bbox)

# Combine the data frames into a single object
all_bboxes <- do.call(rbind, bbox_list)

# Print the combined bounding box data frame
print(all_bboxes)
