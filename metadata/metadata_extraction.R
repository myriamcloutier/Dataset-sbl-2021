####
# Run functions in stac_functions.R.
# Here is how to use those functions to extract metadata from local tif files.
####

library("gdalcubes")
library("rstac")
library("raster")


#### To extract the bounding box in a loop ####

# Function to calculate bounding box for a single raster
get_raster_bbox <- function(raster_file) {
  r <- raster(raster_file)
  ext <- extent(r)
  bbox <- data.frame(xmin = as.numeric(ext@xmin), 
                     xmax = as.numeric(ext@xmax),
                     ymin = as.numeric(ext@ymin), 
                     ymax = as.numeric(ext@ymax))
  return(bbox)
}

# List of raster file paths
#raster_files <- c("path/to/1.tif", "path/to/2.tif")
raster_files <- "F:\\Dataset-2021-sbl\\2021-05-28\\zone3\\2021-05-28-sbl-z3-rgb-cog.tif"

# Apply the function to get bounding box for each raster
bbox_list <- lapply(raster_files, get_raster_bbox)

# Combine the data frames into a single object
all_bboxes <- do.call(rbind, bbox_list)

# Print the combined bounding box data frame
print(all_bboxes)




#### To verify the bbox output ####

ortho <- read_stars('F:/Dataset-2021-sbl/2021-05-28/zone3/2021-05-28-sbl-z3-rgb-cog.tif', 
                    proxy = TRUE,
                    NA_value = 0)
plot(ortho, rgb = 1:3) # pour une image couleur

bbox_polygon <- st_as_sf(all_bboxes, coords = c("xmin", "xmax", "ymin", "ymax"))
plot(bbox_polygon)

carto_stat <- tm_shape(ortho) + # on charge notre orthomosaïque
  tm_rgba() + # pour image RGB avec transparence (a)
  tm_shape()
carto_stat

















library("raster")
library("leaflet")

bbox <- all_bboxes

r <- raster("F:\\Dataset-2021-sbl\\2021-05-28\\zone3\\2021-05-28-sbl-z3-rgb-cog.tif")

# Convert bbox to a leaflet map
bbox_map <- leaflet() %>%
  addTiles() %>%
  addRasterImage(r) %>%
  addRectangles(
    lng1 = bbox$xmin,
    lat1 = bbox$ymin,
    lng2 = bbox$xmax,
    lat2 = bbox$ymax,
    color = "red",
    weight = 2
  )

# Display the map
bbox_map

