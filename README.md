This script is importing the assets located under a root folder

Creates Material Instance after a Master Material  (/Game/MasterMaterial/M_MasterMaterial') 

The scanning will look for "source" and "textures" folders

MasterMaterial needs to have 
Texture Parameters for the following inputs : 
"BaseColor": "BaseColor",
"Metallic": "Metallic",
"Normal": "Normal",
"Roughness": "Roughness",
"Emissive" : "Emissive",
"AO" : "AO"

Consequently the files need to have these names in their filename.

**Line 127 root_folder = r'REPLACE WITH YOUR OWN PATH'**
