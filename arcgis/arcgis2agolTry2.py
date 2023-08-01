'''
Publishing a web tile layer on ArcGIS Online with Python

References : https://gis.stackexchange.com/questions/344679/publishing-a-web-tile-layer-on-arcgis-online-with-python

'''

from arcgis.gis import GIS
from atmo.connect import *
from shutil import copyfile
import arcpy
import os

######################

# Connecting to Portal
arcpy.SignInToPortal(url_agol,id_agol,mdp_agol)

# Set output file names
annee = '2018'
ville = 'LILLE'
outdir = dir + '/%s/%s' %(ville,annee)
print(outdir)

service = ville + "_"+annee+"_PM25_moy"
sddraft_file = outdir + '\\' + service + '.sddraft'

##### Step 1 - Creating SDDraft file from ArcGiS Pro project

# Reference map to publish
aprx = arcpy.mp.ArcGISProject(dir + r"/ARCGIS_projects/" + ville + '/' + ville + ".aprx")

map = aprx.listMaps("Map")[0]

# Create Tile Layer SharingDraft from map in ArcGisPro project
sharing_draft = map.getWebLayerSharingDraft("HOSTING_SERVER", "TILE", service)
print('Web Layer Sharing Draft was created.')

# Create Service Definition Draft file
sharing_draft.exportToSDDraft(sddraft_file)
print('Service Definition Draft File was created.')


##### Step 2 - Create SD file (Service Definition) from SDDraft file

# Create Service definition file
sd_file = outdir + '\\' + service + ".sd"
arcpy.StageService_server(sddraft_file, sd_file)
print('Service Definition was created.')


##### Step 3 - Publication of the tiles layer from SD file

# Share to portal as Tile Layer
print("Uploading Service Definition...")
arcpy.UploadServiceDefinition_server(sd_file, "My Hosted Services") # connexion to AGOL

print("Successfully Uploaded service.")