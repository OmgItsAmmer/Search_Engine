import json
import mmh3  # MurmurHash3 Python library
import os
from collections import defaultdict


def create_or_update_barrels(input_json, output_directory):
    """
    Processes the input JSON to create barrels for terms, storing hashed term IDs and their associated year-based data.

    Parameters:
    - input_json: Path to the input JSON file containing terms with years and product entries.
    - output_directory: Directory to save the barrel files (one per term prefix).
    """
    try:
        # Ensure the output directory exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Read the JSON file
        print(f"Loading data from {input_json}...")
        with open(input_json, 'r') as json_file:
            data = json.load(json_file)

            # Iterate through the terms (keys of the JSON)
            print("Creating or updating barrels...")
            for term, years in data.items():
                # Get the first three characters of the term (in lowercase)
                prefix = term[:3].lower()

                # Barrel file for the prefix (e.g., "sum.json" for terms starting with "sum")
                barrel_file = os.path.join(output_directory, f"{prefix}.json")

                # Hash the full term to get a unique hash_id for the term
                hash_id = mmh3.hash(term)

                # Load the existing barrel or create a new one
                if os.path.exists(barrel_file):
                    with open(barrel_file, 'r') as barrel:
                        barrel_data = json.load(barrel)
                else:
                    barrel_data = {}

                # Add or update the entry for the current hash_id (the term)
                barrel_data[hash_id] = {}

                # Loop through the years and add the associated values to the hash_id
                for year, values in years.items():
                    if year not in barrel_data[hash_id]:
                        barrel_data[hash_id][year] = []

                    # Append the values to the corresponding year list
                    barrel_data[hash_id][year].extend(values)

                # Save the updated barrel data back to the file
                with open(barrel_file, 'w') as barrel:
                    json.dump(barrel_data, barrel, indent=4)

                print(f"Updated barrel for prefix '{prefix}' with term '{term}' (hash {hash_id})")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
input_json = r"F:\Class\3 rd Semester\DSA\Assignments\Project\Search_Engine\data\processed_data\v4\year_based_hashed_inverted_index2.json" # Path to your input JSON file
output_directory = r"F:\Class\3 rd Semester\DSA\Assignments\Project\Search_Engine\data\processed_data\v4b"  # Directory where barrel files will be saved
create_or_update_barrels(input_json, output_directory)
