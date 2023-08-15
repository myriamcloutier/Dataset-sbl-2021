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
bbox_list <- lapply(raster_files, get_raster_bbox)

# Combine the data frames into a single object
all_bboxes <- do.call(rbind, bbox_list)

# Print the combined bounding box data frame
print(all_bboxes)

# Save file as csv
write.csv(all_bboxes, file = "F:/Dataset-2021-sbl/metadata/all_bboxes.csv")

# Save also as Excel file
library("writexl")
write_xlsx(all_bboxes, "F:/Dataset-2021-sbl/metadata/all_bboxes.xlsx")
