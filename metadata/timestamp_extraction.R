###
# Extracting timestamps from JPG files
# First and last timestamp in folder to get starttime and endtime of drone missions
###

library(jpeg)
library(exifr)

# Function to extract image timestamp using EXIF data

get_image_timestamp <- function(image_path) {
  exif_data <- exifr::exifr(image_path)
  
  if(!is.null(exif_data$DateTimeOriginal)) {
    return(exif_data$DateTimeOriginal)
  } else {
    return(NULL)
  }
}

# Function to process a folder and extract earliest and latest timestamps

process_folder <- function(folder_path) {
  earliest_timestamp <- NULL
  latest_timestamp <- NULL
  
  # Get a list of all files in the folder and its subfolders
  file_list <- list.files(path = folder_path, recursive = TRUE, full.names = TRUE)
  
  # Iterate through the list of files
  for (file in file_list) {
    # Check if the file is a JPEG image
    if (tolower(tools::file_ext(file)) == "jpg") {
      timestamp <- get_image_timestamp(file)
      
      # If the image has a valid timestamp in its EXIF data
      if (!is.null(timestamp)) {
        # Update earliest_timestamp if necessary
        if (is.null(earliest_timestamp) || timestamp < earliest_timestamp) {
          earliest_timestamp <- timestamp
        }
        
        # Update latest_timestamp if necessary
        if (is.null(latest_timestamp) || timestamp > latest_timestamp) {
          latest_timestamp <- timestamp
        }
      }
    }
  }
  
  return(list(earliest_timestamp = earliest_timestamp, latest_timestamp = latest_timestamp))
}


# Define the root folder containing the subfolder with JPEG files

root_folder <- "/lefodata/data/drone_missions/2021-09-02-sbl-cloutier-z3-P4RTK-WGS84"

# Process the root folder to get earliest and latest timestamps
timestamps <- process_folder(root_folder)

# Display the results
if (!is.null(timestamps$earliest_timestamp) && !is.null(timestamps$latest_timestamp)) {
  cat("Earliest timestamp:", timestamps$earliest_timestamp, "\n")
  cat("Latest timestamp:", timestamps$latest_timestamp, "\n")
} else {
  cat("No JPEG files with valid timestamps found.\n")
}








