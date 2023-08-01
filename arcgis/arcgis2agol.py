'''
Automating publishing raster tiles from ArcGIS Pro to ArcGIS Online.

References : https://pro.arcgis.com/en/pro-app/2.9/arcpy/sharing/featuresharingdraft-class.htm

'''

import arcpy
import os

# Sign in to portal
arcpy.SignInToPortal("https://www.arcgis.com", "MyUserName", "MyPassword")

# Set output file names
outdir = r"C:\Users\p1177632\Documents\ArcGIS\Projects\Dataset-sbl-2021\output"
service_name = "FeatureSharingDraftTest2"
sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)
sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

# Reference map to publish
aprx = arcpy.mp.ArcGISProject(r"C:\Users\p1177632\Documents\ArcGIS\Projects\Dataset-sbl-2021\Dataset-sbl-2021.aprx")
m = aprx.listMaps('Map1')[0]

# Create FeatureSharingDraft and set metadata, portal folder, and export data properties
server_type = "HOSTING_SERVER"
service_type = "IMAGE_TILE"
sddraft = m.getWebLayerSharingDraft(server_type, service_type, service_name)
sddraft.summary = "This is summary"
sddraft.tags = "sbl"
sddraft.portalFolder = "2021-Dataset-sbl"
sddraft.allowExporting = True

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

# Stage Service
print("Start Staging")
arcpy.StageService_server(sddraft_output_filename, sd_output_filename)

# Share to portal
print("Start Uploading")
arcpy.UploadServiceDefinition_server(sd_output_filename, server_type)

print("Finish Publishing")