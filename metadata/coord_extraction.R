###
# Extracting coordinates from raster file
###

library(raster)

## From chatGPT, not tested

get_raster_bbox <- function(raster_files) {
  coords_list <- list()
  
  for (file in raster_files) {
    r <- raster(file_test)
    num_cells <- ncell(r)
    xy <- xyFromCell(r, 1:num_cells)
    coords_list[[file]] <- data.frame(x = xy[, 1], y = xy[, 2])
  }
  
  return(coords_list)
}

library(readr)

# Read CSV data
raster_files <- read_csv("file_paths.csv") # name of csv
raster_paths <- raster_files$file_path

# Apply the function to get coordinates for each raster
coords_list <- get_raster_bbox(raster_paths)