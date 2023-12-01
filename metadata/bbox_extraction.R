####
# Extracting bboxes from raster files
####

library("dplyr")
library("raster")
library("tidyverse")

setwd("~/GitHub/Dataset-sbl-2021")

#### To extract the bounding box in a loop ####

# Function to calculate bounding box for a single raster
get_raster_bbox <- function(raster_files) {
  r <- raster(raster_files)
  ext <- extent(r)
  bbox <- data.frame(filename = raster_files,
                     xmin = round(as.numeric(ext@xmin), 2),
                     xmax = round(as.numeric(ext@xmax), 2),
                     ymin = round(as.numeric(ext@ymin), 2),
                     ymax = round(as.numeric(ext@ymax), 2))
  return(bbox)
}

# List of raster file paths

raster_files <- data.frame(read_csv("filenamesann.csv", col_names = FALSE))
raster_files

# Apply the function to get bounding box for each raster
bbox_list_raster <- lapply(raster_files, get_raster_bbox)

# Combine the data frames into a single object
all_bboxes_raster <- do.call(rbind, bbox_list_raster)

# Print the combined bounding box data frame
print(all_bboxes_raster)

# Save file as csv
write.csv(all_bboxes_raster, file = "F:/Dataset-2021-sbl/metadata/all_bboxes_ann.csv")

# Save also as Excel file
library("writexl")
write_xlsx(all_bboxes_raster, "F:/Dataset-2021-sbl/metadata/all_bboxes_ann.xlsx")




###
# Extracting bbox from vector file
###

# Load required libraries
library("sf")
library("readr")

# Set working directory
setwd("~/GitHub/Dataset-sbl-2021")

# Define function to calculate bounding box for a single vector file
get_vector_bbox <- function(vector_files) {
  bbox_list <- list()
  
  # Loop through each vector file
  for (file in vector_files) {
    # Read the GeoJSON vector file using the sf library
    sf_obj <- st_read(file)
    
    # Calculate the bounding box of the vector data
    bbox <- st_bbox(sf_obj)
    
    # Create a data frame with the bounding box coordinates and filename
    bbox_df <- data.frame(filename = file,
                          xmin = round(bbox["xmin"], 2),
                          xmax = round(bbox["xmax"], 2),
                          ymin = round(bbox["ymin"], 2),
                          ymax = round(bbox["ymax"], 2))
    
    # Store the bounding box data frame in a list
    bbox_list[[file]] <- bbox_df
  }
  
  return(bbox_list)
}

# Read the list of vector file paths from a CSV file
vector_files <- data.frame(read_csv("filenamesann.csv", col_names = FALSE))

# Call the function to get bounding box for each vector file
bbox_list_vector <- get_vector_bbox(vector_files)

# Combine the bounding box data frames into a single data frame
all_bboxes_vector <- do.call(rbind, bbox_list_vector)

# Print the combined bounding box data frame
print(all_bboxes_vector)

# Save the combined bounding box data frame as CSV
write.csv(all_bboxes_vector, file = "F:/Dataset-2021-sbl/metadata/all_bboxes_vector.csv")

# Save the combined bounding box data frame as Excel
library("writexl")
write_xlsx(all_bboxes_vector, "F:/Dataset-2021-sbl/metadata/all_bboxes_vector.xlsx")

