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

##### ETAPE 1 - Création du fichier SDDraft depuis un projet ArcGIS Pro

# Reference map to publish
aprx = arcpy.mp.ArcGISProject(dir + r"/ARCGIS_projects/" + ville + '/' + ville + ".aprx")

map = aprx.listMaps("LILLE_PM25_moy")[0]

# Create Tile Layer SharingDraft from map in ArcGisPro project
sharing_draft = map.getWebLayerSharingDraft("HOSTING_SERVER", "TILE", service)
print('Le brouillon de la WebLayer est créé.')

# Create Service Definition Draft file
sharing_draft.exportToSDDraft(sddraft_file)
print('Le fichier du brouillon du service de Définition est créé')


##### ETAPE 2 - Création du fichier SD (Service Definition) depuis le fichier SDDraft

# Create Service definition file
sd_file = outdir + '\\' + service + ".sd"
arcpy.StageService_server(sddraft_file, sd_file)
print('Le fichier de Service définition est créé')


##### ETAPE 3 - Publication de la couche de tuiles depuis le fichier SD

# Share to portal as Tile Layer
print("Uploading Service Definition...")
arcpy.UploadServiceDefinition_server(sd_file, "My Hosted Services") #connexion à AGOL

print("Successfully Uploaded service.")