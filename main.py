import os
from pathlib import Path
import tomllib
from dotenv import load_dotenv

import httpx
import dvuploader as dv

# Constants for output
BOLD = "\033[1m"
RESET = "\033[0m"

def check_dataverse_access(api_token: str, dataverse_url: str, persistent_id: str) -> bool:
    """
    Check if we can access the dataset with the provided credentials.
    Returns True if successful, False otherwise.
    """
    base_url = dataverse_url.rstrip("/")
    test_url = f"{base_url}/api/datasets/:persistentId/?persistentId={persistent_id}"
    headers = {"X-Dataverse-key": api_token}
    
    try:
        response = httpx.get(test_url, headers=headers)
        
        if response.status_code == 401:
            print(f"\n{BOLD}⚠️  Error: Invalid API token.{RESET}")
            print("Please check that your API_TOKEN in .env is correct and has not expired.")
            print(f"You can generate a new token at: {base_url}/dataverseuser.xhtml?selectTab=apiTokenTab\n")
            return False
        
        if response.status_code == 404:
            print(f"\n{BOLD}⚠️  Error: Dataset not found.{RESET}")
            print(f"Could not find dataset: {persistent_id}")
            print("Please check that the persistent_id in config.toml is correct.\n")
            return False
        
        response.raise_for_status()
        return True
    
    except httpx.RequestError as e:
        print(f"\n{BOLD}⚠️  Error: Connection failed.{RESET}")
        print(f"Could not connect to Dataverse at {dataverse_url}")
        print("Please check your internet connection and the dv_url in config.toml.\n")
        return False


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Load configuration from config.toml
    config_path = Path("config.toml")
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    # Settings from config and env files
    API_TOKEN = os.getenv("API_TOKEN")
    DV_URL = config["dataset"]["dv_url"]
    PID = config["dataset"]["persistent_id"]
    N_PARALLEL_UPLOADS = config.get("settings", {}).get("n_parallel_uploads", 2)

    # Check API token before proceeding
    if not API_TOKEN:
        print(f"\n{BOLD}⚠️  Error: API_TOKEN not found in .env file.{RESET}")
        print("Please add your Dataverse API token to the .env file.")
        print("You can generate a new token at: https://datasets.lib.berkeley.edu/dataverseuser.xhtml?selectTab=apiTokenTab\n")
        return
    
    if not check_dataverse_access(API_TOKEN, DV_URL, PID):
        return

    directories = []  # init directories list

    # Process directories from config
    for dir_info in config.get("directories", []):
        dir_path = Path(dir_info["dir_path"])
        
        # Check if the directory exists
        if not dir_path.is_dir():
            print(f"Warning: {dir_path} is not a valid directory. Skipping.")
            continue

        # Add directory to list
        directories.extend(dv.add_directory(dir_path))

    # File metadata settings
    for file_obj in directories:
        file_obj.tab_ingest = False
        file_obj.categories = None

    # Check for valid directories
    if not directories:
        print(f"\n{BOLD}⚠️  No valid directories found to upload. Exiting.{RESET}\n")
        return

    # Upload directories to Dataverse
    dvuploader = dv.DVUploader(files=directories)
    
    try:
        dvuploader.upload(
            api_token=API_TOKEN,
            dataverse_url=DV_URL,
            persistent_id=PID,
            n_parallel_uploads=N_PARALLEL_UPLOADS
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            print(f"\n{BOLD}⚠️  Error: Permission denied.{RESET}")
            print(f"You do not have permission to upload to dataset: {PID}")
            print("Please contact the dataset owner to request upload access.\n")
            return
        raise  # Re-raise if it's a different HTTP error


if __name__ == "__main__":
    main()