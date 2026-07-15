import os
from pathlib import Path
import tomllib
from dotenv import load_dotenv

import dvuploader as dv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Load configuration from config.toml
    config_path = Path("config.toml")
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    directories = [] # init directories list

    # Process directories from config
    for dir_info in config.get("directories", []):
        dir_path = Path(dir_info["dir_path"])
        
        # Check if the directory exists
        if not dir_path.is_dir():
            print(f"Warning: {dir_path} is not a valid directory. Skipping.")
            continue

        # Add directory to list
        directories.append(*dv.add_directory(dir_path))

    # File metadata settings
    for file_obj in directories:
            file_obj.tab_ingest = False
            file_obj.categories = None

    # Check for valid directories
    if not directories:
        print("No valid directories found to upload. Exiting.")
        return
    
    # Settings from config and evn files
    API_TOKEN = os.getenv("API_TOKEN")
    DV_URL = config["dataset"]["dv_url"]
    PID = config["dataset"]["persistent_id"]
    N_PARALLEL_UPLOADS = config["settings"]["n_parallel_uploads"]

    # Upload directories to Dataverse
    dvuploader = dv.DVUploader(files=directories)
    dvuploader.upload(
        api_token=API_TOKEN,
        dataverse_url=DV_URL,
        persistent_id=PID,
        n_parallel_uploads=N_PARALLEL_UPLOADS
    )

if __name__ == "__main__":
    main()
