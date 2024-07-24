import os
import unreal

def log(message):
    """
    Log a message to Unreal's output log.
    """
    unreal.log(message)
################################################
def create_material_instance(base_material_path, texture_files, material_instance_name, destination_path):
    """
    Create a material instance with a given texture.
    """
    # Load the base material
    base_material = unreal.load_asset(base_material_path)
    if not base_material:
        log(f"Base material not found at {base_material_path}")
        return None

    # Create a material instance factory
    factory = unreal.MaterialInstanceConstantFactoryNew()
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_instance = asset_tools.create_asset(material_instance_name, destination_path, unreal.MaterialInstanceConstant, factory)

    # Set the parent material
    material_instance.set_editor_property('parent', base_material)

    # Define texture parameters
    texture_parameters = {
        "BaseColor": "BaseColor",
        "Metallic": "Metallic",
        "Normal": "Normal",
        "Roughness": "Roughness",
        "Emissive" : "Emissive",
        "AO" : "AO"
    }

    # Assign textures to parameters
    for param, tex_name in texture_parameters.items():
        texture = next((unreal.load_asset(tex) for tex in texture_files if tex_name.lower() in tex.lower()), None)
        if texture:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(material_instance, param, texture)
            log(f"Assigned {tex_name} texture to {param} parameter.")
    
    log(f"Created material instance: {material_instance_name} with texture: {texture_files}")
    return material_instance
#############################################
def scan_and_import_assets(root_folder):
    """
    Scan the root folder and import assets based on their categories.
    """
    log(f"Scanning root folder: {root_folder}")
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    log("Created Asset Tools object.")

    for category_dir in os.listdir(root_folder):
        category_path = os.path.join(root_folder, category_dir)
        if os.path.isdir(category_path):
            log(f"Processing category: {category_dir}")
            asset_files = {'source': [], 'textures': []}

            for dirpath, _, filenames in os.walk(category_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if 'source' in dirpath.lower():
                        asset_files['source'].append(file_path)
                    elif 'textures' in dirpath.lower():
                        asset_files['textures'].append(file_path)
            
            log(f"Found {len(asset_files['source'])} source files and {len(asset_files['textures'])} texture files in category {category_dir}")

            def import_assets(files, destination_path):
                if files:
                    asset_import_data = unreal.AutomatedAssetImportData()
                    asset_import_data.destination_path = destination_path
                    asset_import_data.filenames = files
                    asset_import_data.replace_existing = True
                    result = asset_tools.import_assets_automated(asset_import_data)
                    log(f"Imported {len(result)} assets to {destination_path}")
                    return result
                return []

            imported_meshes = import_assets(asset_files['source'], f'/Game/ImportTest/{category_dir}/')
            imported_textures = import_assets(asset_files['textures'], f'/Game/ImportTest/{category_dir}/')

            # Apply textures to meshes
            for mesh in imported_meshes:
                mesh_name = os.path.splitext(os.path.basename(mesh.get_path_name()))[0]
                material_instance_name = f"MI_{mesh_name}"
                material_instance_path = f'/Game/ImportTest/{category_dir}'

                # Assuming there's only one texture per category for simplicity
                if imported_textures:
                    texture_files = [texture.get_path_name() for texture in imported_textures]
                    material_instance = create_material_instance('/Game/MasterMaterial/M_MasterMaterial', texture_files, material_instance_name, material_instance_path)
                    if material_instance:
                        apply_material_to_mesh(mesh.get_path_name(), material_instance)

#######################
def apply_material_to_mesh(mesh_path, material_instance):
    """
    Apply the material instance to the mesh.
    """
    mesh = unreal.load_asset(mesh_path)
    if not mesh:
        log(f"Mesh not found at {mesh_path}")
        return False

    unreal.EditorAssetLibrary.save_asset(mesh.get_path_name())
    mesh.set_material(0, material_instance)
    unreal.EditorAssetLibrary.save_asset(mesh.get_path_name())
    log(f"Applied material to mesh: {mesh_path}")
    return True

# Root folder address
root_folder = r'REPLACE WITH YOUR OWN PATH'

# Scan and import new assets
scan_and_import_assets(root_folder)
