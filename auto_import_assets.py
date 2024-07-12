import os
import unreal

def log(message):
    """
    Log a message to Unreal's output log.
    """
    unreal.log(message)

def scan_and_import_assets(root_folder):
    """
    Scan the root folder and import assets based on their categories.
    """
    # Create asset tools object
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    log("Created Asset Tools object.")

    for subdir, _, _ in os.walk(root_folder):
        if subdir == root_folder:
            continue
        
        category_name = os.path.basename(subdir)
        asset_files = {'source': [], 'textures': []}

        # Traverse the subdirectory structure
        for dirpath, _, filenames in os.walk(subdir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if 'source' in dirpath.lower():
                    asset_files['source'].append(file_path)
                elif 'textures' in dirpath.lower():
                    asset_files['textures'].append(file_path)
        
        # Define a function to import assets
        def import_assets(files, destination_path):
            if files:
                assetImportData = unreal.AutomatedAssetImportData()
                assetImportData.destination_path = destination_path
                assetImportData.filenames = files
                assetImportData.replace_existing = True
                assetTools.import_assets_automated(assetImportData)
        
        # Import source files
        import_assets(asset_files['source'], f'/Game/ImportTest/{category_name}')
        
        # Import texture files
        import_assets(asset_files['textures'], f'/Game/ImportTest/{category_name}')

# Define the root folder
root_folder = r'ADD YOUR ROOT FOLDER PATH HERE'

# Run the function to scan and import assets
scan_and_import_assets(root_folder)
