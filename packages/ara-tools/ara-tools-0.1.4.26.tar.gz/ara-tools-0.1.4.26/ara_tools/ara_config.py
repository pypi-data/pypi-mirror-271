from pydantic import BaseModel
import json
import os
from typing import List

# Define a Pydantic model for ARA configuration
class ARAconfig(BaseModel):
    code_dirs: List[str] = ["./src"]
    steps_dir: str = "./ara/features/steps"
    tests_dir: str = "./tests"
    glossary_dir: str = "./glossary"
    doc_dir: str = "./docs"
    local_prompt_templates_dir: str = "./ara/.araconfig/prompt-modules"
    local_ara_templates_dir: str = "./ara/.araconfig/ara_templates"

# Function to ensure the necessary directories exist
def ensure_directory_exists(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"New directory created at {directory}")
    return directory

# Function to read the JSON file and return an ARAconfig model
def read_data(filepath: str) -> ARAconfig:
    if not os.path.exists(filepath):
        # If file does not exist, create it with default values
        default_config = ARAconfig()
        with open(filepath, 'w') as file:
            json.dump(default_config.model_dump(), file, indent=4)
        print(f"ara-tool configuration file '{filepath}' created with default configuration. Please modify it as needed and re-run your command")
        exit()  # Exit the application

    with open(filepath, 'r') as file:
        data = json.load(file)
    return ARAconfig(**data)

# Function to modify the configuration data
def modify_data(config: ARAconfig) -> ARAconfig:
    # Example modification: add a new code directory
    config.code_dirs.append("./new_code_dir")
    # Change the tests directory
    config.tests_dir = "./new_tests_dir"
    return config

# Function to save the modified configuration back to the JSON file
def save_data(filepath: str, config: ARAconfig):
    with open(filepath, 'w') as file:
        json.dump(config.dict(), file, indent=4)


# Singleton for configuration management
class ConfigManager:
    _config_instance = None

    @classmethod
    def get_config(cls, filepath='./ara/.araconfig/ara_config.json'):
        if cls._config_instance is None:
            cls._config_instance = read_data(filepath)
        return cls._config_instance

# # Main script operations
# if __name__ == "__main__":
#     # Ensure the configuration directory exists
#     config_directory = ensure_directory_exists('./ara/.araconfig')
#     file_path = os.path.join(config_directory, 'ara_config.json')  # Full path to your JSON configuration file

#     config = read_data(file_path)
#     if config:  # Only proceed if the file already existed and was read successfully
#         modified_config = modify_data(config)
#         save_data(file_path, modified_config)
#         print("Configuration updated successfully!")
