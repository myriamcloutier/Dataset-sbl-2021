####
# Extracting bboxes from raster files
####

library("dplyr")
library("raster")
library("tidyverse")

setwd("~/GitHub/Dataset-sbl-2021")

#### To extract the bounding box in a loop ####

# #Function to calculate bounding box for a single raster
# get_raster_bbox <- function(raster_paths) {
#   r <- raster(raster_paths)
#   ext <- extent(r)
#   bbox <- data.frame(filename = raster_paths,
#                      xmin = round(as.numeric(ext@xmin), 2),
#                      xmax = round(as.numeric(ext@xmax), 2),
#                      ymin = round(as.numeric(ext@ymin), 2),
#                      ymax = round(as.numeric(ext@ymax), 2))
#   return(bbox)
# }

get_raster_bbox <- function(raster_file) {
  b <- brick(raster_file)
  ext <- extent(b)
  bbox <- data.frame(filename = raster_file,
                     xmin = round(as.numeric(ext@xmin), 2),
                     xmax = round(as.numeric(ext@xmax), 2),
                     ymin = round(as.numeric(ext@ymin), 2),
                     ymax = round(as.numeric(ext@ymax), 2))
  return(bbox)
}


# # List of raster file paths
# raster_files <- data.frame(read_csv("filenamesrgb.csv", col_names = FALSE))
# raster_files

raster_files <- read_csv("filenamesrgb_block.csv", col_names = FALSE)

# # Load the rasters
# raster_list <- lapply(raster_files$file_path, raster)
# raster_list

raster_paths <- raster_files$X1

# Apply the function to get bounding box for each raster
bbox_list <- lapply(raster_paths, get_raster_bbox)

# Combine the data frames into a single object
all_bboxes <- do.call(rbind, bbox_list)

# Print the combined bounding box data frame
print(all_bboxes)

# Save file as csv
write.csv(all_bboxes, file = "F:/Dataset-2021-sbl/metadata/all_bboxes.csv")

# Save also as Excel file









#First version that worked

setwd("~/GitHub/Dataset-sbl-2021")

#### To extract the bounding box in a loop ####

# Function to calculate bounding box for a single raster
get_raster_bbox <- function(raster_files) {
  r <- raster(raster_files)
  ext <- extent(r)
  bbox <- data.frame(filename = raster_files, 
                     xmin = as.numeric(ext@xmin),
                     xmax = as.numeric(ext@xmax),
                     ymin = as.numeric(ext@ymin), 
                     ymax = as.numeric(ext@ymax))
  return(bbox)
}

# List of raster file paths

raster_files <- data.frame(read_csv("filenamesrgb_block.csv", col_names = FALSE))
raster_files

raster_paths <- raster_files$X1


# Apply the function to get bounding box for each raster
bbox_list <- lapply(raster_paths, get_raster_bbox)

# Print the combined bounding box data frame
print(all_bboxes)

# Save file as csv
write.csv(all_bboxes, file = "F:/Dataset-2021-sbl/metadata/all_bboxes.csv")








library(raster)
library(readr)

get_raster_bbox <- function(raster_file) {
  r <- raster(raster_file)
  ext <- extent(r)
  bbox <- data.frame(filename = raster_file, 
                     xmin = as.numeric(ext@xmin),
                     xmax = as.numeric(ext@xmax),
                     ymin = as.numeric(ext@ymin), 
                     ymax = as.numeric(ext@ymax))
  return(bbox)
}

raster_files <- read_csv("filenamesrgb.csv", col_names = TRUE)

bbox_list <- lapply(raster_files$file_path, get_raster_bbox)

all_bboxes <- do.call(rbind, bbox_list)

















