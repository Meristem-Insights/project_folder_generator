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

def copy_readme(source_path, destination_path):
    """Copy README file if it exists."""
    if source_path and os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
        
def check_readme_requirement(folder_name, folder_structure):
    """Check if a README is required for a folder and warn if missing."""
    folder_parts = folder_name.split("/")
    folder_config = folder_structure
    for part in folder_parts:
        folder_config = folder_config.get(part, {})
    return folder_config.get("readme_required", False)

def create_folders(base_path, folder_structure, readme_folder):
    """Recursively create folders and copy README files if required."""
    for folder, contents in folder_structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        # Check if this folder requires a README
        readme_required = check_readme_requirement(folder, folder_structure)
        if readme_required:
            # Check for corresponding README file
            readme_file = os.path.join(readme_folder, f"{folder}.md")
            if os.path.exists(readme_file):
                copy_readme(readme_file, os.path.join(folder_path, "README.md"))
            else:
                print(f"Warning: No README file found for folder '{folder}'")
        
        # Recursively create subfolders if there are any
        if isinstance(contents, dict):
            create_folders(folder_path, contents, readme_folder)

def get_existing_clients(directory):
    """Get a list of folder names in the specified directory."""
    if os.path.exists(directory):
        return [f.name for f in os.scandir(directory) if f.is_dir()]
    return []

def main():
    # Get the root folder name dynamically from the user input
    root_folder_name = input("Enter the root folder name (e.g., 'client'): ")

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
    elif client_status != "new":
        print("Invalid input. Please enter either 'new' or 'existing'.")
        return


    # Extract the folder structure for the selected root folder
    folder_structure = pfg_config.get('ra_folder_structure', {}).get(root_folder_name, {})


    base_path = "./output_structure"  # Change this to your desired root directory
    create_folders(base_path, folder_structure, readme_folder)
    print("Folder structure created successfully.")

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
root_folder_name = input("Enter the root folder name (e.g., 'client'): ")

# Extract the folder structure under 'ra_folder_structure'
folder_structure = pfg_config.get('ra_folder_structure', {}).get(root_folder_name, {})

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
