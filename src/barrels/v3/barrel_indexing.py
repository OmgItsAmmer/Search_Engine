import json
import os

# Path to barrel directory
BARREL_DIRECTORY = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\barrels\alphabateical_barrels\v3"
INDEX_FILE = r"C:\Users\ammer\OneDrive\Desktop\SearchEngine\data\processed_data\barrels\alphabateical_barrels\barrel_index_v3\barrel_index.json"  # Output file for barrel index

def create_and_save_barrel_index(directory, index_file):
    """Scan barrel directory and save index to a JSON file."""
    # Create the barrel index
    barrel_index = {
        os.path.splitext(file)[0]: os.path.join(directory, file)
        for file in os.listdir(directory) if file.endswith('.json')
    }

    # Save the index to a JSON file
    with open(index_file, 'w') as json_file:
        json.dump(barrel_index, json_file, indent=4)

    print(f"Barrel index saved to {index_file}")


if __name__ == "__main__":
    # Create and save the barrel index
    create_and_save_barrel_index(BARREL_DIRECTORY, INDEX_FILE)
