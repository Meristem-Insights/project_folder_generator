# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 08:24:30 2025

@author: Scotty Lumb

the purpose of this script is to generate a project folder automatically and insert readmes into each folder
"""

#################################
#################################
#################################
## IMPORTS
#################################
#################################
#################################

import os
import yaml
import shutil

#################################
#################################
#################################
## fxns
#################################
#################################
#################################


def copy_readmes(base_path, readme_folder):
    for dirpath, dirnames, _ in os.walk(base_path):
        for dirname in dirnames:
            # Try to match the folder name with a README file
            readme_filename = f"readme_{dirname}.md"  # e.g., readme_analysis.md for analysis folder
            readme_src = os.path.join(readme_folder, readme_filename)
            readme_dest = os.path.join(dirpath, dirname, "README.md")
            
            if os.path.exists(readme_src):
                shutil.copy(readme_src, readme_dest)
            else:
                print(f"Warning: No README found for folder: {dirname}")

# def copy_readme(source_path, destination_path):
#     """Copy README file if it exists."""
#     if source_path and os.path.exists(source_path):
#         shutil.copy(source_path, destination_path)

        
def check_readme_requirement(folder_name, folder_structure):
    """Check if a README is required for a folder and warn if missing."""
    folder_parts = folder_name.split("/")
    folder_config = folder_structure
    for part in folder_parts:
        if not isinstance(folder_config, dict):
            return False
        folder_config = folder_config.get(part, {})
    if isinstance(folder_config, dict):
        return folder_config.get("readme_required", False)
    return False


# def check_readme_requirement(folder_name, folder_structure):
#     """Check if a README is required for a folder and warn if missing."""
#     folder_parts = folder_name.split("/")
#     folder_config = folder_structure
#     for part in folder_parts:
#         folder_config = folder_config.get(part, {})
#     return folder_config.get("readme_required", False)

def create_folders(base_path, folder_structure):
    """Recursively create folders and copy README files if required."""
    for folder, contents in folder_structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)


        # Recursively create subfolders if there are any
        if isinstance(contents, dict):
            create_folders(folder_path, contents)

def get_existing_clients(directory):
    """Get a list of folder names in the specified directory."""
    if os.path.exists(directory):
        return [f.name for f in os.scandir(directory) if f.is_dir()]
    return []


def main():
    # Ask the user if the client is new or existing
    client_status = input("Is the client new or existing? (new/existing): ").lower()
    
    if client_status == "existing":
        # List existing client folders in P:\ and let the user select one
        print("\nExisting clients:")
        existing_clients = get_existing_clients(r'P:\\')
        if existing_clients:
            for idx, client in enumerate(existing_clients, 1):
                print(f"{idx}. {client}")
            client_choice = int(input("\nSelect a client by number: ")) - 1
            if 0 <= client_choice < len(existing_clients):
                root_folder_name = existing_clients[client_choice]
                print(f"\nProceeding with existing client '{root_folder_name}'")
            else:
                print("Invalid selection.")
                return
        else:
            print("No existing clients found in P:\\.")
            return
    elif  client_status == "new":
        root_folder_name = input("enter new client name: ")
    else:
        print("Invalid input. Please enter either 'new' or 'existing'.")
        return

    # Get the project folder name from the user
    project_name = input("Enter the project folder name (e.g., 'TSA_evaluation'): ")

    # # Load the folder structure from YAML
    # with open('pfg_config.yaml', "r", encoding="utf-8") as f:
    #     pfg_config = yaml.safe_load(f)
    
    base_structure = pfg_config.get('ra_folder_structure', {}).get("client", {})

    # Set the folder structure based on the selected project
    folder_structure = {project_name: base_structure.get("project_folder", {})}

    # Create the base path for the new project
    # base_path = f"P:\\{root_folder_name}\\{project_name}"
    base_path = f"P:\\{root_folder_name}"
    # Create the folder structure
    create_folders(base_path, folder_structure)
    print("Folder structure created successfully.")

    # Copy the corresponding README files
    readme_folder = "P:\\RA\\project_folder_generator\\readmes"  # Adjust this path as needed
    copy_readmes(f"P:\\{root_folder_name}\\{project_name}", readme_folder)
    print("README files copied successfully.")

# def main():


#     # Ask the user if the client is new or existing
#     client_status = input("Is the client new or existing? (new/existing): ").lower()
    
#     if client_status == "existing":
#         # List existing client folders in P:\ and let the user select one
#         print("\nExisting clients:")
#         existing_clients = get_existing_clients(r'P:\\')
#         if existing_clients:
#             for idx, client in enumerate(existing_clients, 1):
#                 print(f"{idx}. {client}")
#             client_choice = int(input("\nSelect a client by number: ")) - 1
#             if 0 <= client_choice < len(existing_clients):
#                 root_folder_name = existing_clients[client_choice]
#                 print(f"\nProceeding with existing client '{root_folder_name}'")
#             else:
#                 print("Invalid selection.")
#                 return
#         else:
#             print("No existing clients found in P:\\.")
#             return
#     elif client_status != "new":
#         print("Invalid input. Please enter either 'new' or 'existing'.")
#         return

#     # Get the root folder name dynamically from the user input
#     project_name = input("Enter the project folder name (e.g., 'TSA evaluation'): ")

#     base_structure = pfg_config.get('ra_folder_structure', {}).get("client", {})
    
    
#     folder_structure = {project_name: base_structure.get("project_folder", {})}


#     # Extract the folder structure for the selected root folder
#     # folder_structure = pfg_config.get('ra_folder_structure', {}).get("client", {})


#     # base_path = "./output_structure"  # Change this to your desired root directory
#     base_path = f"P:\\{root_folder_name}"
    
#     create_folders(base_path, folder_structure, readme_folder)
#     print("Folder structure created successfully.")

#################################
#################################
#################################
## GLOBAL VARIABLES
#################################
#################################
#################################


with open(r'P:\RA\project_folder_generator\pfg_config.yaml', "r", encoding="utf-8") as f:
    pfg_config = yaml.safe_load(f)
    
# Get the root folder name dynamically from the user input
# root_folder_name = input("Enter the root folder name (e.g., 'client'): ")

# Extract the folder structure under 'ra_folder_structure'
# folder_structure = pfg_config.get('ra_folder_structure', {}).get(root_folder_name, {})

# Folder structure should now be dynamic based on user input

readme_folder = "readmes"  # Folder where README files are stored

#################################
#################################
#################################
## run behaviour
#################################
#################################
#################################



#################################
#################################
#################################
## run
#################################
#################################
#################################

if __name__ == "__main__":
    main()
