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

raster_files <- data.frame(read_csv("filenamesrgb_block.csv", col_names = FALSE))
raster_files


# Apply the function to get bounding box for each raster
bbox_list_raster <- lapply(raster_files, get_raster_bbox)

# Combine the data frames into a single object
all_bboxes_raster <- do.call(rbind, bbox_list_raster)

# Print the combined bounding box data frame
print(all_bboxes_raster)

# Save file as csv
write.csv(all_bboxes_raster, file = "F:/Dataset-2021-sbl/metadata/all_bboxes_raster.csv")

# Save also as Excel file
library("writexl")
write_xlsx(all_bboxes_raster, "F:/Dataset-2021-sbl/metadata/all_bboxes_raster.xlsx")







###
# Extracting bbox from vector file
###

library("sf")
library("readr")

setwd("~/GitHub/Dataset-sbl-2021")

#### To extract the bounding box in a loop ####

# Function to calculate bounding box for a single raster
get_vector_bbox <- function(vector_files) {
  bbox_list <- list()
  
  for (file in vector_files) {
    sf_obj <- st_read(file)
    bbox <- st_bbox(sf_obj)
    bbox_df <- data.frame(filename = file,
                          xmin = round(bbox["xmin"], 2),
                          xmax = round(bbox["xmax"], 2),
                          ymin = round(bbox["ymin"], 2),
                          ymax = round(bbox["ymax"], 2))
    bbox_list[[file]] <- bbox_df
  }
  
  return(bbox_list)
}

# List of raster file paths

vector_files <- data.frame(read_csv("filenamesPol.csv", col_names = FALSE))
vector_files


# Apply the function to get bounding box for each raster
#bbox_list <- lapply(vector_files, get_vector_bbox)
bbox_list_vector <- get_vector_bbox(vector_files)


# Combine the data frames into a single object
all_bboxes_vector <- do.call(rbind, bbox_list_vector)

# Print the combined bounding box data frame
print(all_bboxes_vector)

# Save file as csv
write.csv(all_bboxes_vector, file = "F:/Dataset-2021-sbl/metadata/all_bboxes_vector.csv")

# Save also as Excel file
library("writexl")
write_xlsx(all_bboxes_vector, "F:/Dataset-2021-sbl/metadata/all_bboxes_vector.xlsx")

