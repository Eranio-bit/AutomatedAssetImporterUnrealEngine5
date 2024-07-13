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
    log(f"Scanning root folder: {root_folder}")
    
    # Create asset tools object
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    log("Created Asset Tools object.")

    for category_dir in os.listdir(root_folder):
        category_path = os.path.join(root_folder, category_dir)
        if os.path.isdir(category_path):
            log(f"Processing category: {category_dir}")
            asset_files = []

            # Traverse subdirectories for source and texture files
            for dirpath, _, filenames in os.walk(category_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    asset_files.append(file_path)
            
            log(f"Found {len(asset_files)} files in category {category_dir}")

            # Define a function to import assets
            def import_assets(files, destination_path):
                if files:
                    assetImportData = unreal.AutomatedAssetImportData()
                    assetImportData.destination_path = destination_path
                    assetImportData.filenames = files
                    assetImportData.replace_existing = True
                    result = assetTools.import_assets_automated(assetImportData)
                    log(f"Imported {len(result)} assets to {destination_path}")

            # Import all files under the category folder
            import_assets(asset_files, f'/Game/ImportTest/{category_dir}/')

# Define the root folder
root_folder = r'ADD ROOT PATH FOLDER HERE'

# Run the function to scan and import assets
scan_and_import_assets(root_folder)
